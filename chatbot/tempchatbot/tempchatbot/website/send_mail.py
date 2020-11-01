import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAIL_SERVER = 'email.vmware.com'
MAIL_FROM = 'aupadhaya@vmware.com'


def send_mail(subject, message, msg_to):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = msg_to

    HTML_BODY = MIMEText(message, 'text')
    msg.attach(HTML_BODY)

    smtpObj = smtplib.SMTP(MAIL_SERVER)
    smtpObj.sendmail(MAIL_FROM, msg_to, msg.as_string())

# if __name__ == '__main__':
#     msg= "Test mail"
#     print( send_mail(msg,"moneyg@vmware.com") )
