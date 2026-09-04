from typing import Tuple, Optional
from werkzeug.security import generate_password_hash
from models.user import User
from validators.user_validator import UserValidator
from repositories.user_repository import UserRepository
from services.email_service import EmailService


class UserService:
    """
    Capa de Lógica de Negocio / Casos de Uso (Orquestador de Aplicación).
    Aplica el Principio de Inversión de Dependencias (DIP) y Responsabilidad Única (SRP).
    """

    def __init__(
        self,
        user_repository: UserRepository,
        email_service: Optional[EmailService] = None,
        validator: type[UserValidator] = UserValidator,
    ):
        self.user_repository = user_repository
        self.email_service = email_service or EmailService()
        self.validator = validator

    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        age_str: str,
        password: str,
        confirm_password: str,
    ) -> Tuple[bool, str, Optional[User]]:
        """
        Ejecuta el flujo completo de registro de un usuario:
        1. Valida reglas de negocio de los campos.
        2. Verifica que el correo no esté duplicado.
        3. Encripta la contraseña de forma segura.
        4. Persiste la entidad en el repositorio.
        5. Notifica vía correo electrónico de confirmación.

        Retorna:
            (success: bool, message: str, user: Optional[User])
        """
        # 1. Validación de datos
        is_valid, validation_error, age_int = self.validator.validate_registration(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age_str=age_str,
            password=password,
            confirm_password=confirm_password,
        )

        if not is_valid:
            return False, validation_error, None

        # 2. Verificación de unicidad de correo
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            return False, "Este correo electrónico ya está registrado.", None

        # 3. Hasheo seguro de la contraseña
        password_hash = generate_password_hash(password)

        # 4. Creación y persistencia de la Entidad
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age_int,
            password_hash=password_hash,
        )

        try:
            saved_user = self.user_repository.save(new_user)
        except Exception as e:
            return False, f"Error al guardar usuario en la base de datos: {str(e)}", None

        # 5. Envío del correo de confirmación (no bloqueante)
        try:
            self.email_service.send_welcome_email(
                recipient_email=saved_user.email,
                first_name=saved_user.first_name,
            )
        except Exception as e:
            print(f"[USER SERVICE WARNING] Error al enviar correo: {e}")

        return True, "Usuario registrado exitosamente.", saved_user
