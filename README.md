# Sistema de Registro de Usuarios con Flask y SQLite

Aplicación web desarrollada en **Python (Flask)** con persistencia en **SQLite** y gestión a través de **DataGrip**. Presenta una interfaz moderna con estilo *glassmorphism* en una paleta de colores **rojo, negro y blanco**, iconografía vectorial SVG profesional, validaciones robustas sincronizadas en cliente y servidor, y plantilla personalizada de confirmación.

---

## 📋 Apartado de Cambios y Actualizaciones Recientes

### 1. Migración de Base de Datos y Herramientas de Gestión
- **Cambio de Motor de Base de Datos**: Migración del motor de base de datos a **SQLite**, simplificando el despliegue local y la portabilidad del proyecto.
- **Gestión con DataGrip**: Se adoptó **JetBrains DataGrip** como entorno de desarrollo y administración de base de datos (reemplazando el panel web de Supabase) para la ejecución de scripts SQL, consulta de esquemas y visualización de tablas.

### 2. Actualización de Reglas de Validación (Frontend y Backend)
Se agregaron e implementaron dos reglas de validación fundamentales:

- **Regla 1: Validación de Mayoría de Edad (18 a 100 años)**:
  - **Frontend (`main.js` / `index.html`)**: Restricción en el campo numérico con atributos `min="18" max="100"` y comprobación en JavaScript que bloquea envíos de usuarios menores de 18 años.
  - **Backend (`app.py`)**: Validación estricta que comprueba que la edad convertida a entero cumpla `18 <= edad <= 100`. De no cumplirse, emite el mensaje: *"Debes tener al menos 18 años (y un máximo de 100 años) para registrarte."*
- **Regla 2: Fortaleza y Complejidad de Contraseña**:
  - **Frontend (`main.js` / `index.html`)**: Exigencia de longitud mínima de 8 caracteres (`minlength="8"`), mensaje de ayuda contextual y validación con expresión regular `/^(?=.*[A-Za-z])(?=.*\d).{8,}$/` (requiere al menos una letra y al menos un número).
  - **Backend (`app.py`)**: Validación con el módulo `re` (`re.search(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$", password)`). En caso de no cumplir el criterio, emite el mensaje: *"La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número."*

### 3. Rediseño Visual y Experiencia de Usuario (UI/UX)
- **Paleta Rojo, Negro y Blanco**: Modernización total del diseño con fondos oscuros profundos (`#09090b` / `#121216`), acentos en rojo moderno (`#ef4444` / `#b91c1c`), tarjetas translúcidas y tipografía nítida en blanco.
- **Iconos SVG Profesionales**: Sustitución de todos los emojis por iconos vectoriales SVG limpios para cada campo (usuario, correo, calendario, seguridad/candado) y alertas.
- **Visor de Contraseña Dinámico**: Alternancia interactiva entre iconos SVG de visibilidad (ojo abierto / ojo tachado).
- **Limpieza de Interfaz**: Se removieron la insignia superior previa y el enlace inferior de inicio de sesión.
- **Formularios Claros**: Se retiró el prefijo "Ej." en todos los placeholders del formulario.

---

## 📁 Estructura del Proyecto

```text
Actividad_Formulario_Ingenieria_Software_I/
├── app.py                  # Servidor Flask y controlador de registro con validaciones
├── requirements.txt        # Dependencias de Python (Flask, python-dotenv, etc.)
├── .env                    # Variables de entorno y configuración
├── .env.example            # Plantilla de ejemplo para variables de entorno
├── schema.sql              # Script SQL con la definición de tablas para SQLite / DataGrip
├── email_template.html     # Plantilla HTML responsiva para confirmación de correo
├── templates/
│   ├── index.html          # Formulario de registro (UI Glassmorphism Rojo/Negro/Blanco)
│   └── success.html        # Pantalla de confirmación y pasos de activación
└── static/
    ├── css/
    │   └── style.css       # Hoja de estilos moderna (Variables, animaciones, SVG styling)
    └── js/
        └── main.js         # Lógica interactiva en cliente (validaciones y toggle de contraseña)
```

---

## 🚀 Pasos para Configurar y Ejecutar

### 1. Gestión de Base de Datos en DataGrip
1. Abre **DataGrip** y crea una nueva conexión seleccionando el controlador **SQLite**.
2. Especifica el archivo de base de datos local (por ejemplo `database.db` o el archivo configurado).
3. Abre el archivo [`schema.sql`](file:///c:/Users/josue/OneDrive/Documents/University/Semesters/Sixth%20Semester/Ingenier%C3%ADa%20de%20Software%20I/Actividad_Formulario_Ingenieria_Software_I/schema.sql) dentro de DataGrip y ejecuta el script para inicializar la tabla de usuarios.

### 2. Configurar Entorno Virtual e Instalar Dependencias
Abre una terminal de PowerShell en el directorio raíz del proyecto:

```powershell
# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Iniciar el Servidor Flask
Con el entorno virtual activado, ejecuta:

```powershell
python app.py
```

Abre tu navegador web e ingresa a: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**
