import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Tuple
from flask import render_template


class EmailService:
    """
    Servicio de Notificación por Correo Electrónico (Single Responsibility & Interface Segregation).
    Maneja el despacho de correos electrónicos vía protocolo SMTP y renderizado de plantillas.
    """

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "").strip()
        self.smtp_port_str = os.getenv("SMTP_PORT", "587").strip()
        self.smtp_username = os.getenv("SMTP_USERNAME", "").strip()
        self.smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
        self.sender_name = os.getenv("SMTP_SENDER_NAME", "Sistema de Registro").strip()
        self.sender_email = os.getenv("SMTP_SENDER_EMAIL", self.smtp_username).strip()
        self.use_tls = os.getenv("SMTP_USE_TLS", "true").strip().lower() in ("true", "1", "yes")
        self.use_ssl = os.getenv("SMTP_USE_SSL", "false").strip().lower() in ("true", "1", "yes")

    def send_welcome_email(
        self,
        recipient_email: str,
        first_name: str,
        confirmation_url: str = "http://127.0.0.1:5000/",
    ) -> Tuple[bool, str]:
        """
        Envía un correo electrónico de bienvenida y verificación utilizando SMTP
        y la plantilla HTML templates/email_template.html.
        """
        # Si no se han configurado credenciales de SMTP, registrar en consola amigablemente
        if not self.smtp_server or not self.smtp_username or not self.smtp_password:
            msg = (
                "[MAILER INFO] Configuración SMTP incompleta en .env. "
                "El usuario fue registrado en la base de datos pero el correo no fue despachado."
            )
            print(msg)
            return False, msg

        try:
            smtp_port = int(self.smtp_port_str)
        except ValueError:
            smtp_port = 587

        try:
            # 1. Renderizar contenido HTML dinámico
            html_content = render_template(
                "email_template.html",
                first_name=first_name,
                email=recipient_email,
                confirmation_url=confirmation_url,
            )

            # 2. Versión de texto plano como respaldo
            text_content = (
                f"¡Hola {first_name}!\n\n"
                f"Gracias por registrarte en nuestro sistema con el correo {recipient_email}.\n"
                f"Para verificar tu cuenta, por favor visita el siguiente enlace:\n"
                f"{confirmation_url}\n\n"
                f"Si no solicitaste este registro, puedes ignorar este mensaje.\n"
            )

            # 3. Construir mensaje MIME multipart
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Confirma tu cuenta - ¡Bienvenido {first_name}!"
            msg["From"] = formataddr((self.sender_name, self.sender_email))
            msg["To"] = recipient_email

            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part1)
            msg.attach(part2)

            # 4. Conexión y despacho SMTP
            if self.use_ssl or smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_server, smtp_port, timeout=15)
            else:
                server = smtplib.SMTP(self.smtp_server, smtp_port, timeout=15)
                if self.use_tls:
                    server.starttls()

            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.sender_email, [recipient_email], msg.as_string())
            server.quit()

            print(f"[MAILER SUCCESS] Correo de confirmación enviado exitosamente a {recipient_email}")
            return True, "Correo enviado correctamente."

        except Exception as e:
            error_msg = f"[MAILER ERROR] Falló el envío de correo a {recipient_email}: {str(e)}"
            print(error_msg)
            return False, error_msg
