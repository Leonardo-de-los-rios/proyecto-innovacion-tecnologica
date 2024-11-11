import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a tu base de datos en Neon DB
conn_string = os.environ["NEON_DB"]

try:
    # Establecer conexión
    conn = psycopg2.connect(conn_string)

    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()

    # Ejecutar una consulta de prueba
    cursor.execute("SELECT version();")

    # Obtener el resultado
    db_version = cursor.fetchone()
    print(f"Connected to database: {db_version}")

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")
