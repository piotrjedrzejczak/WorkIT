from flask_mail import Message
from . import mail, app


def send_mail(body, subject, recipient):
    mail.send(
        Message(
            subject=subject,
            recipients=recipient,
            html=body.encode('utf_8'),
            sender=app.config['MAIL_USERNAME']
        )
    )
