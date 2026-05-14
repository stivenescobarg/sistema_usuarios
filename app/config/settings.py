# app/config/settings.py
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno del sistema
load_dotenv()

# ── Configuración general de la aplicación ──────────────────────────────────
APP_NAME    = os.getenv("APP_NAME", "Sistema Usuarios")
APP_VERSION = os.getenv("APP_VERSION", "1.0")

# ── Configuración del administrador ─────────────────────────────────────────
ADMIN_USER  = os.getenv("ADMIN_USER", "admin")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@sistema.com")

# ── Límites del sistema ──────────────────────────────────────────────────────
MAX_USERS = int(os.getenv("MAX_USERS", "100"))