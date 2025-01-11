# db.py
import psycopg2
from psycopg2 import sql

# Conexión a la base de datos PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="your_host",         # Reemplaza con tu host de Neon
        database="your_database", # Nombre de tu base de datos
        user="your_username",     # Nombre de usuario de tu base de datos
        password="your_password"  # Contraseña de tu base de datos
    )
    return conn
