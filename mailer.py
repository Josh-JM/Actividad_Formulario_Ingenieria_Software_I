"""
Módulo de compatibilidad para el despacho de correos electrónicos.
Delega a la clase EmailService ubicada en services/email_service.py.
"""
from services.email_service import EmailService

# Instancia singleton para uso directo si es necesario
_default_email_service = EmailService()


def send_welcome_email(recipient_email: str, first_name: str, confirmation_url: str = None) -> tuple[bool, str]:
    """Función de conveniencia compatible con implementaciones previas."""
    if confirmation_url:
        return _default_email_service.send_welcome_email(
            recipient_email=recipient_email,
            first_name=first_name,
            confirmation_url=confirmation_url,
        )
    return _default_email_service.send_welcome_email(
        recipient_email=recipient_email,
        first_name=first_name,
    )
