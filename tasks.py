from email.message import EmailMessage

from celery import Celery
import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

client = Celery('task', broker='redis://localhost:6379/0', backend='redis://localhost')


@client.task()
def send_mail(email, token, name):
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = 'Activate Account'
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(f"Hello {name}, \n Click the Link to activate your account "
                    f"http://127.0.0.1:5000/activate_email?activate={token}")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(msg)