import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def enviarEmail(self, titulo, texto, destinatario):
        msg = MIMEMultipart()
        msg['From'] = 'notasprofessor@agendabpkedu.space'
        msg['To'] = destinatario
        msg['Subject'] = titulo

        msg.attach(MIMEText(texto, 'html'))

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
