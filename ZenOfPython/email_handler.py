import email
import smtplib
import imaplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart


class MailHandler:
    def __init__(self, login, password, recipients, subject, allowed_header, GMAIL_SMTP="smtp.gmail.com",
                 GMAIL_IMAP="imap.gmail.com"):
        self.login = login
        self.password = password
        self.recipients = recipients
        self.subject = subject
        self.allowed_header = allowed_header

        self.letters_current_header = 0
        self.last_letter = -1
        self.raw_mail = 1

        self.GMAIL_SMTP = GMAIL_SMTP
        self.GMAIL_IMAP = GMAIL_IMAP

    def prepare_letter(self, message):
        our_letter = MIMEMultipart()
        our_letter['From'] = self.login
        our_letter['To'] = ', '.join(self.recipients)
        our_letter['Subject'] = self.subject
        our_letter.attach(MIMEText(message))

        return our_letter

    def send_mail(self, message):
        our_letter = self.prepare_letter(message)

        mail_system = smtplib.SMTP(self.GMAIL_SMTP, 587)
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
        mail_listening = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail_listening.login(self.login, self.password)
        mail_listening.list()
        mail_listening.select("inbox")

        allowed_header = self.allowed_header if self.allowed_header else 'ALL'
        criterion = f'(HEADER Subject "{allowed_header}")'

        _, received_letters = mail_listening.uid('search', None, criterion)
        assert received_letters[self.letters_current_header], 'There are no letters with current header'

        latest_email_uid = received_letters[self.letters_current_header].split()[self.last_letter]
        _, received_letters = mail_listening.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = received_letters[self.letters_current_header][self.raw_mail]
        email_message = email.message_from_string(raw_email)
        print(email_message)
        mail_listening.logout()  # end recieve


if __name__ == '__main__':
    login = 'login@gmail.com'
    password = 'qwerty'
    subject = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    message = 'Message'
    header = None
    GMAIL_IMAP = "imap.gmail.com"
    GMAIL_SMTP = "smtp.gmail.com"

    mail_handler = MailHandler(login=login, password=password, subject=subject, recipients=recipients, message=message,
                               header=header, GMAIL_IMAP=GMAIL_IMAP, GMAIL_SMTP=GMAIL_SMTP)
