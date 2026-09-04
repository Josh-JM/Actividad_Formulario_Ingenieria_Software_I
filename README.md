# Sistema de Registro de Usuarios con Flask, SQLite y Arquitectura Limpia (SOLID)

### 👥 Integrantes
- **Gelber Daniel Clemente Lopez**
- **Josue André Menéndez Juárez**

---

Aplicación web desarrollada en **Python (Flask)** con persistencia en **SQLite** y gestión a través de **DataGrip**. Presenta una arquitectura modular desacoplada basada en principios **SOLID** y el patrón **Boundary - Control - Entity (Clean MVC)**, interfaz moderna con estilo *glassmorphism* en paleta **rojo, negro y blanco**, validaciones robustas y **envío automatizado de correos de confirmación vía SMTP**.

---

## 🏛️ Arquitectura del Sistema y Principios SOLID

El sistema fue refactorizado para eliminar dependencias cíclicas y garantizar un flujo de dependencias estrictamente unidireccional:

1. **Boundary (Capa de Presentación)**:
   - `templates/` (`index.html`, `success.html`, `email_template.html`) y archivos estáticos (`static/`).
   - Rutas web en `app.py` que delegan inmediatamente al controlador.
2. **Control (Capa de Aplicación y Casos de Uso)**:
   - `controllers/user_controller.py`: `UserController` (captura solicitudes HTTP y coordina respuestas).
   - `services/user_service.py`: `UserService` (orquesta el caso de uso de registro de usuarios).
3. **Domain / Entity (Capa de Dominio)**:
   - `models/user.py`: Entidad `User` que modela la estructura de datos del usuario.
   - `validators/user_validator.py`: `UserValidator` (Principio SRP para validación de campos, edad y contraseñas).
4. **Infrastructure (Capa de Datos y Notificaciones)**:
   - `repositories/user_repository.py`: `UserRepository` (Acceso a datos y persistencia en SQLite).
   - `services/email_service.py`: `EmailService` (Despacho SMTP y renderizado de correos).

---

## 📋 Apartado de Cambios y Actualizaciones Recientes

### 1. Refactorización Arquitectónica y Principios SOLID
- **Eliminación de Relación Cíclica**: Desacoplamiento total entre vistas (*Boundary*) y controladores (*Control*).
- **Responsabilidad Única (SRP)**: Cada módulo (`Validator`, `Repository`, `Service`, `Controller`, `Model`) atiende un único propósito.
- **Inversión de Dependencias (DIP)**: La lógica de negocio (`UserService`) recibe sus dependencias inyectadas (`UserRepository`, `EmailService`), permitiendo fácil sustitución y pruebas unitarias.

### 2. Sistema de Envío de Correos Automatizado (SMTP)
- **Despacho Automático de Correos**: Integración del servicio SMTP (`services/email_service.py` / `mailer.py`) que despacha el correo de bienvenida y verificación inmediatamente después del registro.
- **Plantilla HTML Responsiva**: Renderizado dinámico de [`templates/email_template.html`](templates/email_template.html) con Jinja2, incluyendo saludo personalizado, detalles de la cuenta y enlace de confirmación.
- **Configuración Segura vía `.env`**: Compatible con cualquier proveedor SMTP (Gmail, Outlook, Mailtrap, Brevo, etc.).

### 3. Migración de Base de Datos y Herramientas de Gestión
- **Cambio de Motor de Base de Datos**: Migración del motor de base de datos a **SQLite**, simplificando el despliegue local y la portabilidad del proyecto.
- **Gestión con DataGrip**: Se adoptó **JetBrains DataGrip** como entorno de desarrollo y administración de base de datos para la ejecución de scripts SQL, consulta de esquemas y visualización de tablas.

### 4. Actualización de Reglas de Validación (Frontend y Backend)
- **Regla 1: Validación de Mayoría de Edad (18 a 100 años)**:
  - **Frontend (`main.js` / `index.html`)**: Restricción con `min="18" max="100"` y comprobación en JavaScript.
  - **Backend (`validators/user_validator.py`)**: Validación estricta que comprueba que la edad cumpla `18 <= edad <= 100`. De no cumplirse, emite: *"Debes tener al menos 18 años (y un máximo de 100 años) para registrarte."*
- **Regla 2: Fortaleza y Complejidad de Contraseña**:
  - **Frontend (`main.js` / `index.html`)**: Longitud mínima de 8 caracteres y expresión regular `/^(?=.*[A-Za-z])(?=.*\d).{8,}$/`.
  - **Backend (`validators/user_validator.py`)**: Validación con el módulo `re`. En caso de no cumplir el criterio, emite: *"La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número."*

### 5. Rediseño Visual y Experiencia de Usuario (UI/UX)
- **Paleta Rojo, Negro y Blanco**: Modernización total con fondos oscuros profundos (`#09090b` / `#121216`), acentos en rojo moderno (`#ef4444` / `#b91c1c`), tarjetas translúcidas y tipografía nítida en blanco.
- **Iconos SVG Profesionales**: Iconografía vectorial SVG limpia para cada campo y alertas.
- **Visor de Contraseña Dinámico**: Alternancia interactiva entre iconos SVG de visibilidad.

---

## 📁 Estructura del Proyecto

```text
Actividad_Formulario_Ingenieria_Software_I/
├── app.py                          # Punto de entrada, configuración de Flask e inyección de dependencias
├── mailer.py                       # Módulo facade de compatibilidad para el servicio de correo
├── requirements.txt                # Dependencias de Python (Flask, python-dotenv, etc.)
├── .env                            # Variables de entorno y credenciales locales
├── .env.example                    # Plantilla de ejemplo para variables de entorno
├── schema.sql                      # Script SQL con la definición de tablas para SQLite / DataGrip
├── models/
│   └── user.py                     # [Entity] Entidad de dominio User
├── validators/
│   └── user_validator.py           # [Validator] Reglas de validación de negocio (SRP)
├── repositories/
│   └── user_repository.py          # [Repository] Acceso a datos y persistencia SQL
├── services/
│   ├── email_service.py            # [Service] Despacho SMTP y renderizado de correos
│   └── user_service.py             # [Service / Use Case] Orquestador de lógica de registro
├── controllers/
│   └── user_controller.py          # [Control] Controlador de presentación web
├── templates/
│   ├── index.html                  # [Boundary] Formulario de registro (UI Glassmorphism)
│   ├── success.html                # [Boundary] Pantalla de confirmación de registro
│   └── email_template.html         # Plantilla dinámica de confirmación por correo (Jinja2)
└── static/
    ├── css/
    │   └── style.css               # Hoja de estilos moderna (Variables, animaciones, SVG)
    └── js/
        └── main.js                 # Lógica interactiva en cliente (validaciones y toggle)
```

---

## 🚀 Pasos para Configurar y Ejecutar

### 1. Gestión de Base de Datos en DataGrip
1. Abre **DataGrip** y crea una nueva conexión seleccionando el controlador **SQLite**.
2. Especifica el archivo de base de datos local (por ejemplo `database.db`).
3. Abre el archivo [`schema.sql`](schema.sql) dentro de DataGrip y ejecuta el script para inicializar la tabla de usuarios.

### 2. Configuración de Variables de Entorno y Correo (`.env`)
Configura tus credenciales en el archivo `.env`:

```env
# Base de Datos
DATABASE_PATH=sqlite:///database.db
FLASK_SECRET_KEY=dev-super-secret-key

# Configuración SMTP (Ejemplo con Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USE_SSL=False
SMTP_USERNAME=tu_correo@gmail.com
SMTP_PASSWORD=tu_contraseña_de_aplicacion_google
SMTP_SENDER_NAME=Sistema de Registro
SMTP_SENDER_EMAIL=tu_correo@gmail.com
```

### 3. Configurar Entorno Virtual e Instalar Dependencias
Abre una terminal de PowerShell en el directorio raíz del proyecto:

```powershell
# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Iniciar el Servidor Flask
Con el entorno virtual activado, ejecuta:

```powershell
python app.py
```

Abre tu navegador web e ingresa a: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**
