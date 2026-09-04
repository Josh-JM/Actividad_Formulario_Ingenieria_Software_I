import os
import sqlite3
from typing import Optional
from models.user import User


class UserRepository:
    """
    Capa de Acceso a Datos / Repositorio (DIP & SRP).
    Aísla y gestiona todas las operaciones SQL y la persistencia de usuarios en SQLite.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Establece y devuelve una conexión a la base de datos SQLite."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path, timeout=20.0)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self, schema_path: str) -> None:
        """Inicializa las tablas ejecutando el script schema.sql."""
        if os.path.exists(schema_path):
            conn = self.get_connection()
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.close()

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su correo electrónico."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, email, age, password_hash, created_at FROM users WHERE email = ?",
            (email,),
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                age=row["age"],
                password_hash=row["password_hash"],
                created_at=row["created_at"],
            )
        return None

    def save(self, user: User) -> User:
        """
        Inserta un nuevo usuario en la base de datos SQLite y retorna la entidad con su ID asignado.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (first_name, last_name, email, age, password_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user.first_name, user.last_name, user.email, user.age, user.password_hash),
        )
        conn.commit()
        user.id = cursor.lastrowid
        conn.close()
        return user
