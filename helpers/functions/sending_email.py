import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict
from fastapi import HTTPException
from config.mail_config import SMTP_CONFIG

def get_smtp_config():
    return SMTP_CONFIG

def send_email_with_template(smtp_config: Dict, sender_email: str, sender_password: str, recipient_email: str, subject: str, email_user_name: str, template_path: str, activate_path: str):
    try:
        # Leer la plantilla HTML
        with open(template_path, "r") as file:
            email_template = file.read()

        # Reemplazar las variables en la plantilla
        email_body = email_template.replace("{{ user_name }}", email_user_name)
        email_body = email_body.replace("{{ user_email }}", recipient_email)
        email_body = email_body.replace("{{ activate_path }}", activate_path)

        # Configurar el servidor SMTP
        smtp_server = smtp_config["server"]
        smtp_port = smtp_config["port"]
        
        # Crear el mensaje de correo electrónico
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'html'))

        # Iniciar la conexión SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Autenticar con el servidor SMTP
        server.login(sender_email, sender_password)

        # Enviar el correo electrónico
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Cerrar la conexión SMTP
        server.quit()

        return True
    except Exception as e:
        # Manejar cualquier error que ocurra durante el envío del correo electrónico
        print(f"Error al enviar el correo electrónico: {str(e)}")
        return False
