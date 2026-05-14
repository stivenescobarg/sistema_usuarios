# main.py
"""
Punto de entrada del Sistema Modular de Gestión de Usuarios.
Carga la configuración desde .env y muestra un menú interactivo en consola.
"""

from app.config.settings import APP_NAME, APP_VERSION, ADMIN_USER, ADMIN_EMAIL
from app.usuarios.gestor import GestorUsuarios
from app.usuarios.validaciones import (
    ErrorNombreInvalido,
    ErrorEdadInvalida,
    ErrorEmailInvalido,
    ErrorUsuarioDuplicado,
    ErrorLimiteAlcanzado,
)


# ── Helpers de presentación ──────────────────────────────────────────────────

def encabezado():
    """Imprime el encabezado de la aplicación con datos del .env."""
    print("\n" + "=" * 50)
    print(f"  {APP_NAME}  v{APP_VERSION}")
    print(f"  Admin: {ADMIN_USER} | {ADMIN_EMAIL}")
    print("=" * 50)


def menu():
    """Imprime el menú de opciones."""
    print("\n--- MENÚ PRINCIPAL ---")
    print("  1. Registrar usuario")
    print("  2. Listar usuarios")
    print("  3. Buscar usuario")
    print("  4. Eliminar usuario")
    print("  5. Salir")
    print("-" * 22)


def separador():
    print("-" * 40)


# ── Acciones del menú ────────────────────────────────────────────────────────

def accion_registrar(gestor: GestorUsuarios):
    print("\n[ REGISTRAR NUEVO USUARIO ]")
    try:
        nombre = input("  Nombre    : ")
        edad   = input("  Edad      : ")
        email  = input("  Email     : ")

        usuario = gestor.registrar(nombre, edad, email)

        print(f"\n  ✔ Usuario registrado exitosamente:")
        print(f"    ID     : {usuario['id']}")
        print(f"    Nombre : {usuario['nombre']}")
        print(f"    Edad   : {usuario['edad']}")
        print(f"    Email  : {usuario['email']}")

    except (ErrorNombreInvalido, ErrorEdadInvalida, ErrorEmailInvalido) as e:
        print(f"\n  ✘ Error de validación: {e}")
    except ErrorUsuarioDuplicado as e:
        print(f"\n  ✘ Usuario duplicado: {e}")
    except ErrorLimiteAlcanzado as e:
        print(f"\n  ✘ Límite alcanzado: {e}")


def accion_listar(gestor: GestorUsuarios):
    print("\n[ LISTA DE USUARIOS ]")
    usuarios = gestor.listar()

    if not usuarios:
        print("  (No hay usuarios registrados aún)")
        return

    print(f"  Total: {gestor.total()} usuario(s)\n")
    separador()
    print(f"  {'ID':<4} {'Nombre':<20} {'Edad':<6} {'Email'}")
    separador()
    for u in usuarios:
        print(f"  {u['id']:<4} {u['nombre']:<20} {u['edad']:<6} {u['email']}")
    separador()


def accion_buscar(gestor: GestorUsuarios):
    print("\n[ BUSCAR USUARIO ]")
    termino = input("  Ingresa nombre o email a buscar: ").strip()

    if not termino:
        print("  ✘ Debes ingresar un término de búsqueda.")
        return

    resultados = gestor.buscar(termino)

    if not resultados:
        print(f"  No se encontraron usuarios con '{termino}'.")
        return

    print(f"\n  Se encontraron {len(resultados)} resultado(s):\n")
    separador()
    print(f"  {'ID':<4} {'Nombre':<20} {'Edad':<6} {'Email'}")
    separador()
    for u in resultados:
        print(f"  {u['id']:<4} {u['nombre']:<20} {u['edad']:<6} {u['email']}")
    separador()


def accion_eliminar(gestor: GestorUsuarios):
    print("\n[ ELIMINAR USUARIO ]")
    email = input("  Ingresa el email del usuario a eliminar: ").strip()

    try:
        usuario = gestor.eliminar(email)
        print(f"\n  ✔ Usuario '{usuario['nombre']}' eliminado correctamente.")
    except ValueError as e:
        print(f"\n  ✘ {e}")


# ── Bucle principal ──────────────────────────────────────────────────────────

def main():
    encabezado()
    gestor = GestorUsuarios()

    opciones = {
        "1": accion_registrar,
        "2": accion_listar,
        "3": accion_buscar,
        "4": accion_eliminar,
    }

    while True:
        menu()
        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "5":
            print(f"\n  ¡Hasta luego! Gracias por usar {APP_NAME}.\n")
            break
        elif opcion in opciones:
            opciones[opcion](gestor)
        else:
            print("  ✘ Opción inválida. Por favor elige entre 1 y 5.")


if __name__ == "__main__":
    main()