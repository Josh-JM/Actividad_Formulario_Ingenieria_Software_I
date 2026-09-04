from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Entidad de Dominio que representa a un usuario registrado en el sistema."""
    first_name: str
    last_name: str
    email: str
    age: int
    password_hash: str
    id: Optional[int] = None
    created_at: Optional[str] = None
