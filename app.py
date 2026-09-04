import os
from flask import Flask
from dotenv import load_dotenv

from repositories.user_repository import UserRepository
from services.email_service import EmailService
from services.user_service import UserService
from controllers.user_controller import UserController

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()

# 2. Inicializar la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-dev")

# 3. Configuración de la ruta de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
_raw_db = os.getenv("DATABASE_PATH", "database.db").strip()

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
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

# 4. Inyección de Dependencias (Principios SOLID: DIP & SRP)
user_repository = UserRepository(db_path=DATABASE_PATH)
user_repository.init_db(schema_path=SCHEMA_PATH)

email_service = EmailService()
user_service = UserService(user_repository=user_repository, email_service=email_service)
user_controller = UserController(user_service=user_service)


# 5. Enrutamiento Web (Boundary / Delegación al Controlador)
@app.route("/", methods=["GET"])
def index():
    return user_controller.show_registration_form()


@app.route("/register", methods=["POST"])
def register():
    return user_controller.handle_registration()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
