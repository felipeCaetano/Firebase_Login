import os

from dotenv import load_dotenv
import smtplib


load_dotenv()


def account_login(email_server):
    email = os.environ["EMAIL_URL"]
    password = os.environ["EMAIL_KEY"]
    print(email, password)
    email_server.login(email, password)


def get_email_server():
    email_server = smtplib.SMTP("smtp.gmail.com", 587)
    email_server.starttls()
    account_login(email_server)
    return email_server