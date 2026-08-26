import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-dev")

# Configurar Cliente de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client: Client = None

if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "https://your-project-id.supabase.co":
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error al inicializar cliente de Supabase: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    age = request.form.get("age", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    # Validaciones básicas de campos vacíos
    if not all([first_name, last_name, email, age, password, confirm_password]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("index"))

    # Validar coincidencia de contraseña
    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("index"))

    # Validar edad numérica
    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            flash("Ingresa una edad válida.", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("La edad debe ser un número entero.", "error")
        return redirect(url_for("index"))

    # Verificar si el cliente de Supabase está configurado
    if not supabase_client:
        flash(
            "Configura tus credenciales SUPABASE_URL y SUPABASE_KEY en el archivo .env antes de registrarte.",
            "error",
        )
        return redirect(url_for("index"))

    try:
        # Registrar el usuario en Supabase Auth enviando los metadatos
        # Supabase enviará automáticamente el correo de verificación configurado
        response = supabase_client.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "age": age_int,
                    }
                },
            }
        )

        if response.user:
            return render_template("success.html", email=email)
        else:
            flash("No se pudo completar el registro. Inténtalo nuevamente.", "error")
            return redirect(url_for("index"))

    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg:
            flash("Este correo electrónico ya está registrado.", "error")
        else:
            flash(f"Error al registrar usuario: {error_msg}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
