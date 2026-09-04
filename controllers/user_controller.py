from flask import render_template, request, redirect, url_for, flash, Response
from services.user_service import UserService


class UserController:
    """
    Capa de Controlador (Controlador Web / Application Controller).
    Coordina las interacciones entre la capa de presentación (Boundary) y la lógica de negocio (Service).
    """

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def show_registration_form(self) -> str:
        """Muestra el formulario principal de registro (Boundary: index.html)."""
        return render_template("index.html")

    def handle_registration(self) -> Response | str:
        """Procesa la solicitud POST de registro de usuario."""
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        age = request.form.get("age", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Delegar la ejecución a la capa de servicio (Control / Use Case)
        success, message, user = self.user_service.register_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            age_str=age,
            password=password,
            confirm_password=confirm_password,
        )

        if not success:
            flash(message, "error")
            return redirect(url_for("index"))

        return render_template("success.html", email=user.email, first_name=user.first_name)
