import os
import asyncpg
from typing import TypeAlias
from dotenv import load_dotenv

# load the env variables from the  .env file
load_dotenv()

# Define el tipo DbPool para la inyección de dependencias.
DbPool = asyncpg.Pool

# Configuración de la base de datos
CONFIG = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT'))
}

async def create_db_pool(config: dict) -> DbPool:
    """Crea un pool de conexiones a la base de datos."""
    try:
        pool = await asyncpg.create_pool(
            user=config['user'],
            password=config['password'],
            database=config['db'],
            host=config['host'],
            port=config['port']
        )
        return pool
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
