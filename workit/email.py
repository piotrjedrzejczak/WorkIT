from flask import render_template
from flask_mail import Message
from flask_login import current_user
from workit.model.User import User
from workit import mail


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def generate_email(user):
    user = current_user
    body_template = render_template("test_email.txt", user=user)
    html_template = render_template("test_email.html", user=user)

    send_email(
        "Hello! %s" % current_user.name,
        'work.it@o2.pl',
        [current_user.email],
        body_template.encode('utf_8'),
        html_template.encode('utf_8'),
    )
