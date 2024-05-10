import os
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.email import Email
from auth.auth import get_user_from_request
from models.models import User
from helpers.functions.sending_email import send_email_with_template, get_smtp_config

router = APIRouter()

@router.post("/send_email/")
async def send_email(email: Email, smtp_config: dict = Depends(get_smtp_config), user: str = Depends(get_user_from_request), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user == user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    email.user_name = user.name
    email.recipient_email = user.email
    print(f"El usuario es {email.user_name}")
    print(f"Email destino: {email.recipient_email}\
            Asunto: {email.subject}")

    # Obtener la ruta de la carpeta de plantillas desde la variable de entorno
    template_folder = os.getenv("EMAIL_TEMPLATE_FOLDER")

    # Nombre del archivo de la plantilla
    template_filename = "index.html"

    # Construir la ruta completa de la plantilla
    template_path = os.path.join(template_folder, template_filename)

    # Enviar el correo electrónico utilizando la función reutilizable
    if send_email_with_template(smtp_config, smtp_config["sender_email"], smtp_config["sender_password"], email.recipient_email, email.subject, email.user_name, template_path):
        return {"message": "Correo electrónico enviado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al enviar el correo electrónico")
