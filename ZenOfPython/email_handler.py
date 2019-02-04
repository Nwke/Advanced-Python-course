import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

DEFAULT_SMTP = 'smtp.gmail.com'
DEFAULT_IMAP = 'imap.gmail.com'


class MailHandler:
    letters_current_header = 0
    last_letter = -1
    raw_mail = 1

    def __init__(self, login, password, allowed_header, email_smtp=DEFAULT_SMTP,
                 email_iap=DEFAULT_IMAP):
        self.login = login
        self.password = password
        self.allowed_header = allowed_header
        self.email_smtp = email_smtp
        self.email_iap = email_iap

    def prepare_letter(self, message, subject, recipients):
        our_letter = MIMEMultipart()
        our_letter['From'] = self.login
        our_letter['To'] = ', '.join(recipients)
        our_letter['Subject'] = subject
        our_letter.attach(MIMEText(message))

        return our_letter

    def send_mail(self, message, subject, recipients):
        our_letter = self.prepare_letter(message=message, subject=subject,
                                         recipients=recipients)

        mail_system = smtplib.SMTP(self.email_smtp, 587)
        # identify ourselves to smtp gmail client
        mail_system.ehlo()
        # secure our email with tls encryption
        mail_system.starttls()
        # re-identify ourselves as an encrypted connection
        mail_system.ehlo()

        mail_system.login(self.login, self.password)
        mail_system.sendmail(self.login, mail_system, our_letter.as_string())

        mail_system.quit()  # send end

    def receive_mail(self):
        mail_listening = imaplib.IMAP4_SSL(self.email_iap)
        mail_listening.login(self.login, self.password)
        mail_listening.list()
        mail_listening.select("inbox")

        allowed_header = self.allowed_header if self.allowed_header else 'ALL'
        criterion = f'(HEADER Subject "{allowed_header}")'

        _, received_letters = mail_listening.uid('search', None, criterion)
        assert received_letters([self.letters_current_header],
                                'There are no letters with current header')

        latest_email_uid = \
            received_letters[self.letters_current_header].split()[
                self.last_letter]
        _, received_letters = mail_listening.uid('fetch', latest_email_uid,
                                                 '(RFC822)')

        raw_email = received_letters[self.letters_current_header][self.raw_mail]
        email_message = email.message_from_string(raw_email)
        
        print(email_message)
        mail_listening.logout()  # end recieve


if __name__ == '__main__':
    def main():
        login = 'login@gmail.com'
        password = 'qwerty'
        header = None
        email_iap = "imap.gmail.com"
        email_smtp = "smtp.gmail.com"

        mail_handler = MailHandler(login=login, password=password,
                                   allowed_header=header, email_iap=email_iap,
                                   email_smtp=email_smtp)


    main()
