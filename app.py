import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-dev")

# Ruta absoluta de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
_raw_db = os.getenv("DATABASE_PATH", "database.db").strip()

# Soporta tanto nombres de archivo directos como URIs estilo SQLAlchemy (sqlite:///archivo.db)
if _raw_db.startswith("sqlite:////"):
    _clean_db = _raw_db[10:]
elif _raw_db.startswith("sqlite:///"):
    _clean_db = _raw_db[10:]
elif _raw_db.startswith("sqlite://"):
    _clean_db = _raw_db[9:]
elif _raw_db.startswith("sqlite:"):
    _clean_db = _raw_db[7:]
else:
    _clean_db = _raw_db

DATABASE_PATH = _clean_db if os.path.isabs(_clean_db) else os.path.normpath(os.path.join(BASE_DIR, _clean_db))


def get_db_connection():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa la base de datos ejecutando el script schema.sql si es necesario."""
    schema_path = os.path.join(BASE_DIR, "schema.sql")
    if os.path.exists(schema_path):
        conn = get_db_connection()
        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()


# Inicializar la base de datos al arrancar
init_db()


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

    # 1. Validación de campos obligatorios
    if not all([first_name, last_name, email, age, password, confirm_password]):
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for("index"))

    # 2. Validación de coincidencia de contraseñas
    if password != confirm_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect(url_for("index"))

    # Regla de Validación 1: Mayoría de edad (18 a 100 años)
    try:
        age_int = int(age)
        if age_int < 18 or age_int > 100:
            flash(
                "Debes tener al menos 18 años (y un máximo de 100 años) para registrarte.",
                "error",
            )
            return redirect(url_for("index"))
    except ValueError:
        flash("La edad debe ser un número entero válido.", "error")
        return redirect(url_for("index"))

    # Regla de Validación 2: Fortaleza de la contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número)
    if not re.search(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password):
        flash(
            "La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número.",
            "error",
        )
        return redirect(url_for("index"))

    # Hashear contraseña de forma segura
    password_hash = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insertar el nuevo usuario en la base de datos SQLite
        cursor.execute(
            """
            INSERT INTO users (first_name, last_name, email, age, password_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (first_name, last_name, email, age_int, password_hash),
        )
        conn.commit()
        conn.close()

        return render_template("success.html", email=email, first_name=first_name)

    except sqlite3.IntegrityError as e:
        error_msg = str(e)
        if "UNIQUE constraint failed: users.email" in error_msg or "users.email" in error_msg:
            flash("Este correo electrónico ya está registrado.", "error")
        else:
            flash(f"Error de integridad en los datos: {error_msg}", "error")
        return redirect(url_for("index"))

    except Exception as e:
        flash(f"Error al registrar usuario en la base de datos: {str(e)}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
