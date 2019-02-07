import email
import smtplib
import imaplib

from email.message import EmailMessage

DEFAULT_SMTP = 'smtp.yandex.ru'
DEFAULT_IMAP = 'imap.yandex.ru'


class MailHandler:
    letters_current_header = 0
    last_letter = -1
    raw_mail = 1

    def __init__(self, login, password, email_smtp=DEFAULT_SMTP,
                 email_iap=DEFAULT_IMAP):
        self.login = login
        self.password = password
        self.email_smtp = email_smtp
        self.email_iap = email_iap

    def prepare_letter(self, message, subject, recipients):
        our_letter = EmailMessage()
        our_letter['From'] = self.login
        our_letter['To'] = ', '.join(recipients)
        our_letter['Subject'] = subject
        our_letter.set_content(message)

        return our_letter

    def send_mail(self, message, subject, recipients):
        our_letter = self.prepare_letter(message=message, subject=subject,
                                         recipients=recipients)

        mail_server = smtplib.SMTP(self.email_smtp, 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.ehlo()
        mail_server.login(self.login, self.password)
        mail_server.sendmail(self.login, recipients, our_letter.as_bytes())

        mail_server.quit()

    def receive_mail(self, allowed_header='ALL'):
        mail_listening = imaplib.IMAP4_SSL(self.email_iap)
        mail_listening.login(self.login, self.password)
        mail_listening.list()
        mail_listening.select("inbox")

        allowed_header = allowed_header if allowed_header is not None else 'ALL'
        criterion = f'(HEADER Subject "{allowed_header}")'

        _, received_letters = mail_listening.uid('search', None, criterion)
        assert received_letters[
            self.letters_current_header], 'There are no ' \
                                          'letters with current header'

        latest_email_uid = \
            received_letters[self.letters_current_header].split()[
                self.last_letter]
        _, received_letters = mail_listening.uid('fetch', latest_email_uid,
                                                 '(RFC822)')

        raw_email = received_letters[self.letters_current_header][self.raw_mail]
        email_message = email.message_from_bytes(raw_email)

        mail_listening.logout()  # end recieve
        return email_message


def main():
    login = 'example@mail.ru'
    password = 'qwerty'
    header = None
    email_smtp = 'smtp.yandex.ru'
    email_iap = 'imap.yandex.ru'

    mail_system = MailHandler(login=login, password=password,
                              email_iap=email_iap, email_smtp=email_smtp)

    mail_system.send_mail(message='Hello, world', subject='Test message',
                          recipients=['d.blinkovv@yandex.ru'])
    print(mail_system.receive_mail(allowed_header=header))


if __name__ == '__main__':
    main()
