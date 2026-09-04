import re
from typing import Tuple, Optional


class UserValidator:
    """
    Componente de Validación (Principio de Responsabilidad Única - SRP).
    Aplica las reglas de negocio sobre los datos de registro de usuario.
    """

    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d).{8,}$"

    @classmethod
    def validate_registration(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        age_str: str,
        password: str,
        confirm_password: str,
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Valida los campos del formulario de registro.
        
        Retorna:
            (is_valid: bool, error_message: Optional[str], age_int: Optional[int])
        """
        # 1. Validación de campos obligatorios
        if not all([first_name, last_name, email, age_str, password, confirm_password]):
            return False, "Todos los campos son obligatorios.", None

        # 2. Validación de coincidencia de contraseñas
        if password != confirm_password:
            return False, "Las contraseñas no coinciden.", None

        # 3. Regla de Validación 1: Mayoría de edad (18 a 100 años)
        try:
            age_int = int(age_str)
            if age_int < 18 or age_int > 100:
                return (
                    False,
                    "Debes tener al menos 18 años (y un máximo de 100 años) para registrarte.",
                    None,
                )
        except ValueError:
            return False, "La edad debe ser un número entero válido.", None

        # 4. Regla de Validación 2: Fortaleza de la contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número)
        if not re.search(cls.PASSWORD_REGEX, password):
            return (
                False,
                "La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número.",
                None,
            )

        # 5. Formato de correo electrónico
        if not re.match(cls.EMAIL_REGEX, email):
            return False, "El formato del correo electrónico es inválido.", None

        return True, None, age_int
