# from flask_mail import Message
# from workit.model.User import User
# from workit import mail, MAIL_USERNAME
# from flask import render_template, request, redirect, session, url_for, flash
# from flask_login import current_user, login_required, logout_user


# def send_email(subject, sender, recipients, text_body, html_body):
#         msg = Message(subject, sender=sender, recipients=recipients)
#         msg.body = text_body
#         msg.html = html_body
#         mail.send(msg)

# def test_email(name):
#     send_email("Hello! %s" %  name,


#                MAIL_USERNAME[0],
#                [current_user.email],
#                render_template("test_email.txt", 
#                                user=name),
#                render_template("test_email.html", 
#                                user=name))

