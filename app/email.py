from flask_mail imort Message
from app import mail

def send_email(subject, sender, recipients,text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    mail.send(msg)