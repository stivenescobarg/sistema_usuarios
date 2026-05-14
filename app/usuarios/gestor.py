# app/usuarios/gestor.py
from app.usuarios.validaciones import (
    validar_nombre,
    validar_edad,
    validar_email,
    ErrorUsuarioDuplicado,
    ErrorLimiteAlcanzado,
)
from app.config.settings import MAX_USERS


class GestorUsuarios:
    """
    Clase principal para administrar usuarios.
    Almacena los usuarios en una lista de diccionarios en memoria.
    """

    def __init__(self):
        # Lista interna que actúa como "base de datos" en memoria
        self._usuarios: list[dict] = []

    # ── Registrar ────────────────────────────────────────────────────────────

    def registrar(self, nombre: str, edad: str, email: str) -> dict:
        """
        Registra un nuevo usuario tras validar todos sus datos.
        Retorna el diccionario del usuario creado.

        Lanza:
            ErrorLimiteAlcanzado  — si se superó MAX_USERS
            ErrorUsuarioDuplicado — si el email ya existe
            ErrorNombreInvalido   — desde validar_nombre
            ErrorEdadInvalida     — desde validar_edad
            ErrorEmailInvalido    — desde validar_email
        """
        # Verificar límite de usuarios
        if len(self._usuarios) >= MAX_USERS:
            raise ErrorLimiteAlcanzado(
                f"No se pueden registrar más de {MAX_USERS} usuarios."
            )

        # Validar y limpiar cada campo (las funciones lanzan excepción si fallan)
        nombre_valido = validar_nombre(nombre)
        edad_valida   = validar_edad(edad)
        email_valido  = validar_email(email)

        # Verificar que el email no esté duplicado
        if self._buscar_por_email(email_valido):
            raise ErrorUsuarioDuplicado(
                f"Ya existe un usuario registrado con el email '{email_valido}'."
            )

        # Crear el registro
        usuario = {
            "id":     len(self._usuarios) + 1,
            "nombre": nombre_valido,
            "edad":   edad_valida,
            "email":  email_valido,
        }
        self._usuarios.append(usuario)
        return usuario

    # ── Listar ───────────────────────────────────────────────────────────────

    def listar(self) -> list[dict]:
        """Retorna una copia de la lista completa de usuarios."""
        return list(self._usuarios)

    # ── Buscar ───────────────────────────────────────────────────────────────

    def buscar(self, termino: str) -> list[dict]:
        """
        Busca usuarios cuyo nombre o email contenga el término (sin distinción
        de mayúsculas/minúsculas).
        Retorna una lista con los usuarios que coinciden.
        """
        termino = termino.strip().lower()
        resultados = [
            u for u in self._usuarios
            if termino in u["nombre"].lower() or termino in u["email"]
        ]
        return resultados

    # ── Eliminar ─────────────────────────────────────────────────────────────

    def eliminar(self, email: str) -> dict:
        """
        Elimina el usuario que tenga el email indicado.
        Retorna el diccionario del usuario eliminado.
        Lanza ValueError si no se encuentra ningún usuario con ese email.
        """
        email = email.strip().lower()
        usuario = self._buscar_por_email(email)

        if not usuario:
            raise ValueError(
                f"No se encontró ningún usuario con el email '{email}'."
            )

        self._usuarios.remove(usuario)
        return usuario

    # ── Helpers privados ─────────────────────────────────────────────────────

    def _buscar_por_email(self, email: str) -> dict | None:
        """Retorna el usuario con ese email exacto, o None si no existe."""
        for u in self._usuarios:
            if u["email"] == email.lower():
                return u
        return None

    def total(self) -> int:
        """Retorna el número actual de usuarios registrados."""
        return len(self._usuarios)