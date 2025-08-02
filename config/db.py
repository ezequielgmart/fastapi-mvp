"""

db config file

OJO este archivo solo debe de tener la responsabilidad de extraer la info del dot.env y convetirla 
en un config para ser llamado. 

en pyugem se gestionara la conexion. Aqui solo seria traer los datos y crear la conexion para ser exportada. 



"""

import asyncpg
import asyncio
from src.utils.exceptions import EXCEPTIONS

AUTHORS = [
            {
                "author_id": "lkjhgasdfgascnzkquwodanscnzxkcva154",
                "name": "Juan",
                "last_name": "Bosh",
                "nationality": "Dominican",
            },
            {
                "author_id": "wodajhgasdfgascnzkqulknscnzxkcva154",
                "name": "Miguel",
                "last_name": "de Cervates",
                "nationality": "Spain",
            },
            {
                "author_id": "44wo151515dajhgascnzkqulknscnzxkcva15",
                "name": "Adolf",
                "last_name": "Hitler",
                "nationality": "Austria",
            },
        ]


async def check_db_run(config:dict) -> str:
    try:

        conn = await asyncpg.connect(user=config['user'], password=config['password'],
                                    database=config['name'], host=config['host'])
        
        await conn.close() # Cierra la conexión inmediatamente después de verificar

        return EXCEPTIONS['db_connected']
    
    except asyncpg.exceptions.PostgresError as e:

        print(f"Error inesperado al conectar a la base de datos: {e}")
        return f"{EXCEPTIONS['failed_db_con']}"
