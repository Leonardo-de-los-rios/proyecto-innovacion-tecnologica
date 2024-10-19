import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Enlace de conexión a MongoDB
mongo_uri = os.environ["MONGO_DB"]

# Crear una instancia del cliente
client = MongoClient(mongo_uri)

# Seleccionar la base de datos (reemplaza 'nombre_base_datos' con el nombre de tu base de datos)
db = client["nombre_base_datos"]

# Verificar la conexión
try:
    # Listar las colecciones en la base de datos
    collections = db.list_collection_names()
    print("Conexión exitosa. Colecciones disponibles:", collections)
except Exception as e:
    print("Error al conectar con MongoDB:", e)
