import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv
import smtplib

load_dotenv()


class EmailService:
    def send_mail(self, sename, data, hora, temp, press):
        email_server = get_email_server()
        msg = create_email_menssage(sename, data, hora, temp, press)
        try:
            email_server.sendmail(
                os.environ["EMAIL_URL"],
                "felipecmelo@gmail.com",
                msg.as_string())
        except Exception as e:
            print(f"A mensagem falhou: {e}")
        finally:
            email_server.quit()


def account_login(email_server):
    email = os.environ["EMAIL_URL"]
    password = os.environ["EMAIL_KEY"]
    email_server.login(email, password)


def get_email_server():
    email_server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    email_server.starttls()
    account_login(email_server)
    return email_server


def insert_msg_data(sename, data, hora, temp, press):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('email_template.html')

    msg_body = template.render(
        sename=sename,
        data=data,
        hora=hora,
        temp=temp,
        press=[str(disjuntor) for disjuntor in press]
    )
    return msg_body


def create_email_menssage(sename, data, hora, temp, press):
    msg_with_data = insert_msg_data(sename, data, hora, temp, press)
    msg = MIMEMultipart()
    msg['from'] = os.environ["EMAIL_URL"]
    msg['to'] = "felipecmelo@gmail.com"
    msg['subject'] = f"Leitura dos Disjuntores da SE {sename}"
    msg.attach(MIMEText(msg_with_data,"html"))
    return msg
