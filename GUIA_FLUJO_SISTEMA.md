# 📘 Guía de Arquitectura, Flujo y Defensa del Sistema
### Sistema de Registro de Usuarios con Flask, SQLite y Principios SOLID (BCE)

**Autores / Integrantes:**
- Gelber Daniel Clemente Lopez
- Josue André Menéndez Juárez

---

## 🏛️ 1. Arquitectura del Sistema (Patrón BCE y Principios SOLID)

El sistema está estructurado bajo el patrón **Boundary - Control - Entity (BCE)**, garantizando que cada componente tenga una única responsabilidad (**SRP**) y que las dependencias fluyan de manera unidireccional con **Inversión de Dependencias (DIP)**.

```mermaid
graph TD
    User(("👤 Usuario / Navegador"))
    Boundary["🌐 Boundary (templates/ & static/)"]
    App["🚀 app.py (Rutas e Inyección)"]
    Controller["🎮 UserController (controllers/user_controller.py)"]
    Service["⚙️ UserService (services/user_service.py)"]
    Validator["🛡️ UserValidator (validators/user_validator.py)"]
    Repo["💾 UserRepository (repositories/user_repository.py)"]
    Email["📧 EmailService (services/email_service.py)"]
    DB[("🗄️ SQLite database.db")]

    User -->|1. GET / o POST /register| Boundary
    Boundary --> App
    App -->|2. Delegación| Controller
    Controller -->|3. register_user()| Service
    Service -->|4. validate_registration()| Validator
    Service -->|5. find_by_email() / save()| Repo
    Repo --> DB
    Service -->|6. send_welcome_email()| Email
    Service -->|7. Retorno de estado| Controller
    Controller -->|8. render_template()| Boundary
    Boundary -->|9. Respuesta HTML| User
```

---

## 🔄 2. Flujo Completo Paso a Paso (End-to-End)

---

### **Paso 0: Arranque del Servidor e Inyección de Dependencias**
* **Archivo:** `app.py`
* **¿Qué sucede?:**
  1. Carga las variables de entorno desde `.env` (`load_dotenv()`).
  2. Construye la ruta absoluta hacia la base de datos SQLite `database.db`.
  3. **Inyección de Dependencias (DIP):**
     ```python
     user_repository = UserRepository(db_path=DATABASE_PATH)
     user_repository.init_db(schema_path=SCHEMA_PATH)  # Crea la tabla users si no existe

     email_service = EmailService()
     user_service = UserService(user_repository=user_repository, email_service=email_service)
     user_controller = UserController(user_service=user_service)
     ```
  4. Inicia el servidor Flask en `http://127.0.0.1:5000`.

---

### **Paso 1: Solicitud GET inicial (Mostrar Formulario)**
1. **Navegador:** Envía una solicitud HTTP `GET /`.
2. **`app.py`:**
   - La ruta `@app.route("/", methods=["GET"])` intercepta la petición.
   - Ejecuta: `user_controller.show_registration_form()`.
3. **`controllers/user_controller.py`:**
   - La función `show_registration_form()` ejecuta `render_template("index.html")`.
4. **Boundary:** El navegador recibe y muestra `templates/index.html` con sus estilos `static/css/style.css` y validaciones en cliente de `static/js/main.js`.

---

### **Paso 2: Envío de Datos por POST**
1. El usuario completa el formulario y presiona **"Crear Cuenta"**.
2. **Navegador:** Envía una petición `POST /register` con los campos del formulario (`first_name`, `last_name`, `email`, `age`, `password`, `confirm_password`).
3. **`app.py`:**
   - La ruta `@app.route("/register", methods=["POST"])` recibe la petición.
   - Ejecuta: `user_controller.handle_registration()`.

---

### **Paso 3: Controlador extrae datos y delega al Servicio**
* **Archivo:** `controllers/user_controller.py`
* **Función:** `handle_registration()`
* **¿Qué hace?:**
  1. Extrae los valores limpios del formulario con `request.form.get(...)`.
  2. Llama al servicio de negocio pasando los parámetros:
     ```python
     success, message, user = self.user_service.register_user(
         first_name=first_name,
         last_name=last_name,
         email=email,
         age_str=age,
         password=password,
         confirm_password=confirm_password,
     )
     ```

---

### **Paso 4: Orquestación del Caso de Uso (Lógica de Negocio)**
* **Archivo:** `services/user_service.py`
* **Función:** `register_user(...)`
* **Subpasos ejecutados en orden estricto:**

#### 4.1. Validación de Reglas de Negocio
* Llama a: `self.validator.validate_registration(...)` en `validators/user_validator.py`.
* **Reglas comprobadas:**
  - Que no haya ningún campo vacío.
  - Que las contraseñas coincidan (`password == confirm_password`).
  - **Regla de Mayoría de Edad:** Que la edad sea un entero entre **18 y 100 años**.
  - **Regla de Fortaleza de Contraseña:** Mínimo 8 caracteres, al menos 1 letra y 1 número (mediante Regex).
  - Formato válido de correo electrónico con expresión regular.
* *Si falla la validación:* Retorna inmediatamente `(False, error_message, None)`.

#### 4.2. Verificación de Correo Duplicado
* Llama a: `self.user_repository.find_by_email(email)` en `repositories/user_repository.py`.
* Ejecuta en SQLite: `SELECT ... FROM users WHERE email = ?`.
* *Si el usuario ya existe:* Retorna `(False, "Este correo electrónico ya está registrado.", None)`.

#### 4.3. Hasheo Seguro de Contraseña
* Utiliza `generate_password_hash(password)` de la librería `werkzeug.security`.
* La contraseña en texto plano **nunca** se almacena.

#### 4.4. Creación de la Entidad de Dominio
* Instancia el modelo `User` en `models/user.py`:
  ```python
  new_user = User(
      first_name=first_name,
      last_name=last_name,
      email=email,
      age=age_int,
      password_hash=password_hash,
  )
  ```

#### 4.5. Persistencia en Base de Datos (SQLite)
* Llama a: `self.user_repository.save(new_user)`.
* Ejecuta: `INSERT INTO users (first_name, last_name, email, age, password_hash) VALUES (...)`.
* Asigna el ID autoincremental (`user.id = cursor.lastrowid`) y retorna el usuario persistido.

#### 4.6. Despacho Automatizado de Correo Electrónico (SMTP)
* Llama a: `self.email_service.send_welcome_email(recipient_email=saved_user.email, first_name=saved_user.first_name)`.
* En `services/email_service.py`:
  - Renderiza dinámicamente la plantilla `templates/email_template.html` con Jinja2.
  - Construye el mensaje multiparte (HTML y texto plano).
  - Se conecta al servidor SMTP configurado en el `.env` mediante TLS/SSL y despacha el correo.

#### 4.7. Retorno del Servicio
* Retorna: `(True, "Usuario registrado exitosamente.", saved_user)`.

---

### **Paso 5: Respuesta hacia la Vista (Controlador $\rightarrow$ Boundary)**
* **Archivo:** `controllers/user_controller.py`
* **Si `success == False`:**
  - Ejecuta `flash(message, "error")`.
  - Devuelve `redirect(url_for("index"))` para recargar el formulario mostrando la alerta en rojo.
* **Si `success == True`:**
  - Devuelve `render_template("success.html", email=user.email, first_name=user.first_name)`.
  - El navegador muestra la pantalla de éxito con los datos del usuario recién registrado.

---

## 📋 3. Tabla Resumen de Componentes y Funciones

| Capa / Patrón | Archivo | Clase / Módulo | Funciones Principales | Responsabilidad (SRP) |
| :--- | :--- | :--- | :--- | :--- |
| **Boundary** | `templates/index.html`<br>`templates/success.html`<br>`templates/email_template.html` | HTML + Jinja2 | N/A (Vistas) | Presentación e interfaz visual al usuario y diseño de correos. |
| **Boundary (Client)** | `static/js/main.js` | JS Frontend | `togglePasswordVisibility()`<br>Validaciones en tiempo real | Mejorar UX con validaciones interactivas e iconos SVG dinámicos. |
| **Control** | `app.py` | Flask App | `index()`<br>`register()` | Configurar la app, mapear rutas HTTP e inyectar dependencias. |
| **Control** | `controllers/user_controller.py` | `UserController` | `show_registration_form()`<br>`handle_registration()` | Recibir inputs HTTP, llamar al servicio y decidir qué vista renderizar. |
| **Service (Use Case)** | `services/user_service.py` | `UserService` | `register_user(...)` | Orquestar el flujo completo: validación, unicidad, hash, guardado y correo. |
| **Validation** | `validators/user_validator.py` | `UserValidator` | `validate_registration(...)` | Reglas de validación: 18-100 años, password fuerte y formato de correo. |
| **Domain Entity** | `models/user.py` | `User` (dataclass) | N/A (Entidad) | Representar el modelo de datos del Usuario en memoria. |
| **Repository** | `repositories/user_repository.py` | `UserRepository` | `init_db(...)`<br>`find_by_email(...)`<br>`save(...)` | Conexión a SQLite y ejecución de sentencias SQL (`SELECT`, `INSERT`). |
| **Notification** | `services/email_service.py` / `mailer.py` | `EmailService` | `send_welcome_email(...)` | Construcción de plantillas MIME y despacho de correo vía SMTP. |

---

## 🎯 4. Preguntas Frecuentes y Guía de Defensa ante el Docente

### 1. ¿Por qué las funciones en `app.py` solo tienen una línea de código?
> **Respuesta:** *"Para cumplir con la separación de responsabilidades y evitar acoplamiento. `app.py` solo debe actuar como enrutador web y ensamblador de dependencias. Toda la lógica de presentación y manejo de peticiones le pertenece al `UserController`."*

### 2. ¿Por qué no ejecutamos consultas SQL directamente en el Controlador o Servicio?
> **Respuesta:** *"Porque implementamos el **Patrón Repositorio** (`UserRepository`). Al aislar el SQL en el repositorio, la lógica de negocio (`UserService`) se vuelve independiente de la base de datos. Si el día de mañana cambiamos de SQLite a PostgreSQL o MySQL, solo modificamos el repositorio sin alterar ninguna regla de negocio."*

### 3. ¿Cómo se aplica el Principio de Inversión de Dependencias (DIP)?
> **Respuesta:** *"En `app.py`, creamos las instancias de `UserRepository` y `EmailService` y las inyectamos mediante el constructor de `UserService`. La lógica de negocio no crea directamente sus dependencias con rutas duras, sino que las recibe listas para operar, facilitando pruebas unitarias y modularidad."*

### 4. ¿Por qué se valida tanto en JavaScript (`main.js`) como en Python (`user_validator.py`)?
> **Respuesta:** *"La validación en **frontend** mejora la experiencia de usuario (UX) ofreciendo retroalimentación instantánea antes de enviar el formulario. La validación en **backend** es indispensable por seguridad e integridad de datos, evitando que peticiones maliciosas (por ejemplo enviadas desde Postman o cURL) salten los controles del cliente."*

### 5. ¿Por qué usamos DataGrip y SQLite?
> **Respuesta:** *"SQLite ofrece una base de datos ligera, autocontenida y sin necesidad de configurar un servidor externo pesado. Con **DataGrip** podemos gestionar las conexiones, ejecutar el script `schema.sql`, inspeccionar los esquemas y auditar los registros de la tabla `users` de forma visual y profesional."*
