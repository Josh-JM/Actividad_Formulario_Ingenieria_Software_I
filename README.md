# Sistema de Registro de Usuarios con Flask y Supabase

Aplicación web completa desarrollada en **Python (Flask)** con integración a **Supabase (Auth & PostgreSQL)**, diseño en modo oscuro con *glassmorphism*, bordes redondeados, validaciones interactivas en cliente/servidor y envío de correo de confirmación de cuenta personalizado.

---

## 📁 Estructura del Proyecto

```text
Actividad_Formulario_Ingenieria_Software_I/
├── app.py                  # Servidor Flask y controlador de registro con Supabase Auth
├── requirements.txt        # Dependencias de Python (Flask, supabase, python-dotenv)
├── .env                    # Variables de entorno (URL y llaves de API de Supabase)
├── .env.example            # Ejemplo de variables de entorno
├── schema.sql              # Script SQL (ISO/ANSI) para PostgreSQL en Supabase
├── email_template.html     # Plantilla HTML responsiva para confirmación de correo
├── templates/
│   ├── index.html          # Formulario de registro (UI Glassmorphism)
│   └── success.html        # Pantalla de éxito tras enviar el enlace de verificación
└── static/
    ├── css/
    │   └── style.css       # Estilos CSS modernos (Glassmorphism, animaciones, variables)
    └── js/
        └── main.js         # Interactividad JS (mostrar/ocultar contraseña, spinner de carga)
```

---

## 🚀 Pasos para Configurar y Ejecutar

### 1. Configurar la Base de Datos en Supabase
1. Accede a tu consola en [Supabase](https://supabase.com/dashboard).
2. Ve a **SQL Editor** -> **New query**.
3. Copia el contenido del archivo [`schema.sql`](file:///c:/Users/josue/OneDrive/Documents/University/Semesters/Sixth%20Semester/Ingenier%C3%ADa%20de%20Software%20I/Actividad_Formulario_Ingenieria_Software_I/schema.sql) y ejecuta el script (**Run**).

### 2. Configurar la Plantilla de Correo en Supabase
1. En Supabase Dashboard, dirígete a **Authentication** -> **Email Templates** -> **Confirm Signup**.
2. Copia todo el contenido del archivo [`email_template.html`](file:///c:/Users/josue/OneDrive/Documents/University/Semesters/Sixth%20Semester/Ingenier%C3%ADa%20de%20Software%20I/Actividad_Formulario_Ingenieria_Software_I/email_template.html).
3. Pégalo en el cuadro de texto **Body HTML** y guarda los cambios.

### 3. Configurar Credenciales en `.env`
1. En Supabase Dashboard, ve a **Project Settings** -> **API**.
2. Copia tu **Project URL** y tu **anon / public API key**.
3. Reemplázalos en el archivo [`.env`](file:///c:/Users/josue/OneDrive/Documents/University/Semesters/Sixth%20Semester/Ingenier%C3%ADa%20de%20Software%20I/Actividad_Formulario_Ingenieria_Software_I/.env):

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-public-key
```

### 4. Ejecutar la Aplicación Flask Localmente
Abre una terminal en este directorio y ejecuta:

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor Flask
python app.py
```

Abre en tu navegador: [http://127.0.0.1:5000](http://127.0.0.1:5000)
