# app/usuarios/validaciones.py
import re


# ── Excepciones personalizadas ───────────────────────────────────────────────

class ErrorNombreInvalido(Exception):
    """Se lanza cuando el nombre está vacío o contiene caracteres no permitidos."""
    pass


class ErrorEdadInvalida(Exception):
    """Se lanza cuando la edad no es un número entero positivo válido."""
    pass


class ErrorEmailInvalido(Exception):
    """Se lanza cuando el email no tiene el formato correcto."""
    pass


class ErrorUsuarioDuplicado(Exception):
    """Se lanza cuando ya existe un usuario con el mismo email."""
    pass


class ErrorLimiteAlcanzado(Exception):
    """Se lanza cuando se alcanza el número máximo de usuarios permitidos."""
    pass


# ── Funciones de validación ──────────────────────────────────────────────────

def validar_nombre(nombre: str) -> str:
    """
    Valida que el nombre no esté vacío y solo contenga letras y espacios.
    Retorna el nombre limpio (strip) si es válido.
    Lanza ErrorNombreInvalido si no cumple los requisitos.
    """
    nombre = nombre.strip()

    if not nombre:
        raise ErrorNombreInvalido("El nombre no puede estar vacío.")

    if len(nombre) < 2:
        raise ErrorNombreInvalido("El nombre debe tener al menos 2 caracteres.")

    if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+$", nombre):
        raise ErrorNombreInvalido(
            "El nombre solo puede contener letras y espacios. "
            "No se permiten números ni caracteres especiales."
        )

    return nombre


def validar_edad(edad_str: str) -> int:
    """
    Valida que la edad sea un número entero entre 1 y 120.
    Retorna la edad como entero si es válida.
    Lanza ErrorEdadInvalida si no cumple los requisitos.
    """
    try:
        edad = int(edad_str)
    except ValueError:
        raise ErrorEdadInvalida(
            f"'{edad_str}' no es un número válido. La edad debe ser un número entero."
        )

    if edad < 1 or edad > 120:
        raise ErrorEdadInvalida(
            f"La edad {edad} no es válida. Debe estar entre 1 y 120 años."
        )

    return edad


def validar_email(email: str) -> str:
    """
    Valida que el email tenga el formato estándar (usuario@dominio.extension).
    Retorna el email en minúsculas si es válido.
    Lanza ErrorEmailInvalido si no cumple los requisitos.
    """
    email = email.strip().lower()

    if not email:
        raise ErrorEmailInvalido("El email no puede estar vacío.")

    patron = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(patron, email):
        raise ErrorEmailInvalido(
            f"'{email}' no tiene un formato válido. "
            "Ejemplo correcto: usuario@dominio.com"
        )

    return email