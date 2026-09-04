-- =====================================================================
-- ESQUEMA DE BASE DE DATOS LOCAL SQLITE
-- Proyecto: Sistema de Autenticación y Registro de Usuarios
-- Compatible con: SQLite 3 / JetBrains DataGrip
-- =====================================================================

-- 1. CREACIÓN DE LA TABLA DE USUARIOS (ENTIDAD: users)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ÍNDICE ÚNICO PARA OPTIMIZAR BÚSQUEDAS Y VALIDAR DUPLICADOS DE EMAIL
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 3. DISPARADOR (TRIGGER) PARA ACTUALIZAR AUTOMÁTICAMENTE 'updated_at'
CREATE TRIGGER IF NOT EXISTS trg_users_update_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
