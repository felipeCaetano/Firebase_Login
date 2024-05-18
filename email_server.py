import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import smtplib

load_dotenv()


def account_login(email_server):
    email = os.environ["EMAIL_URL"]
    password = os.environ["EMAIL_KEY"]
    print(email, password)
    email_server.login(email, password)


def get_email_server():
    email_server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    email_server.starttls()
    account_login(email_server)
    return email_server


def insert_msg_data(sename, data, hora, temp, press1, press2, press3):
    msg_body = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Leitura de Disjuntores</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f2f2f2;">
            <h2>Boa Tarde,</h2>
        <br>
        <p>Seguem leitura dos disjuntores da SE {sename} no dia {data} - {hora}h com temperatura ambiente de {temp}°C.<p>
        <br>
        <p>14V6 - Pressão SF6: {press1[0]}/{press1[1]}/{press1[2]} bar (Nominal a 20°C 8,0 bar).<br>
        obs: Complementado SF6 pela última vez em 09.04.24.</p>
        <br>
        <p>12T3 - Pressão SF6: {press2[0]}MPa (Nominal a 20°C 0,7MPa).<br>
        obs: Complementado SF6 pela última vez em 19.02.24.</p>
        <br>
        <p>
        12M7 - Pressão SF6: {press3[0]}MPa (Nominal a 20°C 0,7MPa).<br>
        obs: Complementado SF6 pela última vez em 09.09.22.</p>
        
        <br><br>
        <p><strong>enviado com RegistraBGI.</strong></p>
    </body>
    </html>
    """
    return msg_body


def create_email_menssage(sename, data, hora, temp, press1, press2, press3):
    msg_with_data = insert_msg_data(sename, data, hora, temp, press1, press2, press3)
    msg = MIMEMultipart()
    msg['from'] = os.environ["EMAIL_URL"]
    msg['to'] = "chf-OPI_BGI@eletrobras.com"
    msg['subject'] = f"Leitura dos Disjuntores da SE {sename}"
    msg.attach(
        MIMEText(
            msg_with_data,
            "html"
        )
    )
    return msg
