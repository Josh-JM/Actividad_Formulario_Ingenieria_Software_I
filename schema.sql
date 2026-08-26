-- =====================================================================
-- ESTÁNDAR DE NOMENCLATURA Y ESTRUCTURA DE BASE DE DATOS (ISO / ANSI SQL)
-- Proyecto: Sistema de Autenticación y Perfiles de Usuarios en Supabase
-- Versión: 2.0 (Normas Enterprise ISO/IEC 11179 & PostgreSQL Best Practices)
-- =====================================================================

-- 1. CREACIÓN DE LA TABLA DE PERFILES DE USUARIOS (ENTIDAD: app_user_profiles)
-- Utiliza convención snake_case, prefijo de dominio 'app_', claves foráneas explícitas
-- y marcas de tiempo conformes a la norma ISO 8601 (TIMESTAMPTZ).
CREATE TABLE IF NOT EXISTS public.app_user_profiles (
    -- Clave Primaria referenciada a la tabla auth.users de Supabase
    user_id UUID NOT NULL,
    
    -- Atributos de Identificación Personal
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    age SMALLINT NOT NULL,

    -- Marcas de tiempo de auditoría según norma ISO 8601 en UTC
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Definición Explícita de Restricciones (Constraints ISO/ANSI)
    CONSTRAINT pk_app_user_profiles PRIMARY KEY (user_id),
    CONSTRAINT fk_app_user_profiles_auth_users FOREIGN KEY (user_id) 
        REFERENCES auth.users (id) ON DELETE CASCADE,
    CONSTRAINT chk_app_user_profiles_age_range CHECK (age >= 1 AND age <= 120),
    CONSTRAINT chk_app_user_profiles_first_name_length CHECK (char_length(trim(first_name)) >= 2),
    CONSTRAINT chk_app_user_profiles_last_name_length CHECK (char_length(trim(last_name)) >= 2)
);

-- 2. DOCUMENTACIÓN DE TABLA Y COLUMNAS (ISO/IEC 11179 Metadata Standards)
COMMENT ON TABLE public.app_user_profiles IS 'Almacena la información complementaria de perfil para los usuarios autenticados del sistema.';
COMMENT ON COLUMN public.app_user_profiles.user_id IS 'Identificador único universal (UUID ISO/IEC 11578) vinculado a la entidad auth.users.';
COMMENT ON COLUMN public.app_user_profiles.first_name IS 'Nombre(s) de pila del usuario registrado.';
COMMENT ON COLUMN public.app_user_profiles.last_name IS 'Apellido(s) del usuario registrado.';
COMMENT ON COLUMN public.app_user_profiles.age IS 'Edad en años cumplidos (formato entero positivo).';
COMMENT ON COLUMN public.app_user_profiles.created_at IS 'Fecha y hora de creación del registro en formato UTC (ISO 8601).';
COMMENT ON COLUMN public.app_user_profiles.updated_at IS 'Fecha y hora de última modificación del registro en formato UTC (ISO 8601).';

-- 3. HABILITACIÓN DE SEGURIDAD A NIVEL DE FILA (ROW LEVEL SECURITY - RLS)
ALTER TABLE public.app_user_profiles ENABLE ROW LEVEL SECURITY;

-- 4. POLÍTICAS DE SEGURIDAD RLS CON NOMENCLATURA ESTÁNDAR
-- Política de Lectura (SELECT): El usuario solo puede consultar su propio registro
CREATE POLICY policy_app_user_profiles_select_own
    ON public.app_user_profiles
    FOR SELECT
    USING (auth.uid() = user_id);

-- Política de Actualización (UPDATE): El usuario solo puede modificar su propio registro
CREATE POLICY policy_app_user_profiles_update_own
    ON public.app_user_profiles
    FOR UPDATE
    USING (auth.uid() = user_id);

-- 5. FUNCIÓN TRIGGER PARA AUTOMATIZACIÓN DE REGISTRO (PL/pgSQL ISO Standard)
CREATE OR REPLACE FUNCTION public.fn_trg_sync_auth_user_profile()
RETURNS TRIGGER 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.app_user_profiles (
        user_id,
        first_name,
        last_name,
        age,
        created_at,
        updated_at
    )
    VALUES (
        NEW.id,
        COALESCE(NULLIF(TRIM(NEW.raw_user_meta_data->>'first_name'), ''), 'Sin Nombre'),
        COALESCE(NULLIF(TRIM(NEW.raw_user_meta_data->>'last_name'), ''), 'Sin Apellido'),
        COALESCE((NEW.raw_user_meta_data->>'age')::SMALLINT, 18),
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
    RETURN NEW;
EXCEPTION
    WHEN OTHERS THEN
        RAISE WARNING 'Error en fn_trg_sync_auth_user_profile: %', SQLERRM;
        RETURN NEW;
END;
$$;

-- 6. DISPARADOR (TRIGGER) VINCULADO A LA TABLA AUTH.USERS
DROP TRIGGER IF EXISTS trg_on_auth_user_created_sync_profile ON auth.users;

CREATE TRIGGER trg_on_auth_user_created_sync_profile
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_trg_sync_auth_user_profile();

-- 7. FUNCIÓN Y TRIGGER PARA ACTUALIZACIÓN AUTOMÁTICA DE TIMESTAMP (updated_at)
CREATE OR REPLACE FUNCTION public.fn_trg_update_timestamp()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_app_user_profiles_update_timestamp ON public.app_user_profiles;

CREATE TRIGGER trg_app_user_profiles_update_timestamp
    BEFORE UPDATE ON public.app_user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_trg_update_timestamp();
