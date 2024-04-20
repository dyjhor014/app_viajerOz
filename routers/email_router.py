import os
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.email import Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.mail_config import SMTP_CONFIG
from auth.auth import get_user_from_request
from models.models import User

router = APIRouter()

def get_smtp_config():
    return SMTP_CONFIG

@router.post("/send_email/")
async def send_email(email: Email, smtp_config: dict = Depends(get_smtp_config), user: str = Depends(get_user_from_request), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user == user).first()
    email.user_name = user.name
    email.recipient_email = user.email
    print(f"El usuario es {email.user_name}")
    print(f"Email destino: {email.recipient_email}\
            Asunto: {email.subject}")
    # Configurar el servidor SMTP
    smtp_server = smtp_config["server"]
    smtp_port = smtp_config["port"]
    sender_email = smtp_config["sender_email"]
    sender_password = smtp_config["sender_password"]
    
    # Obtener la ruta de la carpeta de plantillas desde la variable de entorno
    template_folder = os.getenv("EMAIL_TEMPLATE_FOLDER")

    # Nombre del archivo de la plantilla
    template_filename = "index.html"

    # Construir la ruta completa de la plantilla
    template_path = os.path.join(template_folder, template_filename)
    
    # Leer la plantilla HTML
    with open(template_path, "r") as file:
        email_template = file.read()

    # Reemplazar las variables en la plantilla
    email_body = email_template.replace("{{ user_name }}", email.user_name)
    email_body = email_body.replace("{{ user_email }}", email.recipient_email)
    
    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email.recipient_email
    msg['Subject'] = email.subject
    msg.attach(MIMEText(email_body, 'html'))
    
    try:
        # Iniciar la conexión SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Autenticar con el servidor SMTP
        server.login(sender_email, sender_password)
        
        # Generar un ID de mensaje único y establecerlo en el encabezado "Message-ID"
        import uuid
        message_id = f"<{uuid.uuid4()}@tekmgr.com>"
        msg['Message-ID'] = message_id
        
        # Enviar el correo electrónico
        server.sendmail(sender_email, email.recipient_email, msg.as_string())
        
        # Cerrar la conexión SMTP
        server.quit()
        
        return {"message": "Correo electrónico enviado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}")
