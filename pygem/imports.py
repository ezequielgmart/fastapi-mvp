"""

este archivo es solo para un test y es para el mvp de extraer la informacion de la base de datos
y luego convetirla en un objeto/clase manipulable para la clase Schema

este objeto manipulable debe de guardarse con todos los de las otras tablas en un archivo en comun 
llamado "imports.db" donde se registren todos objetos instanciados para ser utilizados.

"""

# extraer la data de una bdd
import asyncio
import asyncpg
from asyncpg.pool import Pool
from pathlib import Path
from .pydantic_models import Field
from asyncpg.exceptions import PostgresError


async def create_db_pool(config) -> Pool:
    """Crea y retorna un pool de conexiones a la base de datos."""
    pool = await asyncpg.create_pool(
        min_size=1,     # Número mínimo de conexiones abiertas
        max_size=10,    # Número máximo de conexiones
        loop=None,
        **config
    )
    return pool

class SingleModelSchema:

    def __init__(self, table_name:str, primary_key:str, fields:list):

        self.table = table_name
        self.primary_key = primary_key
        self.fields = fields 


"""

* responsabilidades

r* conectarse a db *
r* extraer metadatos de una tabla en concreto *
r* crear un objeto que represente la tabla * 
r* guardar ese objeto en un archivo 
r* mostrar la informacion. 
r* tomar toda las tablas 
r* la funcion debe de recibir tablas y generar todo el archivo
optimizar a que sea un pool de conexiones en lugar de un conn

"""

# manejar los metodos de la base de datos en pg y las configuracioens. Ideal para iniciar la connecion
class DB: 

    async def start_connection(self, config:dict) -> object:
        
        # conectarse a la db
        conn = await asyncpg.connect(user=config['user'], password=config['password'],database=config['database'], host=config['host'])
        
        return conn
    
class Conn(DB): 

    def __init__(self, config:dict):
        super.__init__()

        self.get = self.start_connection(config)

        
async def get_all_tables(pool:Pool) -> list[str]:
    try:
        # pedir prestada una conexion del pool, se devuelve automaticamente al salir 
        async with pool.acquire() as conn: 
            # 1. Extraer todas las tablas del esquema 'public'
            query_tables = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """
            tables = []
            
            result = await conn.fetch(query_tables)

            for record in result:

                tables.append(record['table_name'])

            
            return tables
        
    except asyncpg.exceptions.PostgresError as e:

        return f"Error connecting the db {e}"


async def get_fields(table:str, pool:Pool) -> dict[str,str,Field]: 
    primary_key_name = ''
    query = """
        SELECT
            c.column_name, c.data_type, c.is_nullable, c.column_default,
            CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'YES' ELSE 'NO' END AS is_primary_key
        FROM
            information_schema.columns AS c
        LEFT JOIN
            information_schema.constraint_column_usage AS ccu ON c.column_name = ccu.column_name
        LEFT JOIN
            information_schema.table_constraints AS tc ON ccu.constraint_name = tc.constraint_name
        WHERE
            c.table_name = $1 AND c.table_schema = 'public'
        ORDER BY
            c.ordinal_position;
    """
    async with pool.acquire() as conn: 
        columns = await conn.fetch(query, table)
        fields = []
        
        for record in columns:
            is_null = record['is_nullable'] != "NO"
            primary_key = record['is_primary_key'] == "YES"
            
            # --- Solución al UnboundLocalError ---
            # Asigna un valor por defecto a data_type al principio del bucle.
            data_type = record['data_type']

            if primary_key:
                primary_key_name = record['column_name']
            
            if record['data_type'] == 'character varying': 
                data_type = "varchar"
            
            field = {
                "is_primary_key": primary_key,
                "name": record['column_name'],
                "type": data_type,
                "is_null": is_null
            }

            # Comprobación de duplicados mejorada
            if not any(f.name == field["name"] for f in fields):
                fields.append(Field(**field))

    result = {"table_name": table, "pk": primary_key_name, "fields": fields}

    return result


# Nueva función para crear un archivo que contiene todos los esquemas
def create_all_migrations_file(all_tables_info: list) -> bool:
    try:
        path = Path("./entities/migrations.py")
        full_content = ""
        header = f"""from pygem.main import SingleGenericSchema
from pygem.pydantic_models import Field\n\n"""
        full_content = header
        
        for table_info in all_tables_info:
            content = migration_file_content(
                table_info["table_name"], 
                table_info["pk"], 
                table_info["fields"]
            )
            full_content += content
            
        with open(path, "w") as file:
            file.write(full_content)
        
        return True
    except Exception as e:
        print(f"Ocurrió un error al crear el archivo de migraciones: {e}")
        return False

# Modificación en la función migration_file_content
# Esta función ahora solo crea el bloque de código para una tabla
def migration_file_content(table: str, primary_key_name: str, fields: list) -> str:
    fields_string_list = [
        f"        Field(is_primary_key={field.is_primary_key}, name='{field.name}', type='{field.type}', is_null={field.is_null})"
        for field in fields
    ]
    formatted_fields = ",\n".join(fields_string_list)
    
    return f"""
_{table}_gem = SingleGenericSchema(
    table='{table}',
    primary_key='{primary_key_name}',
    fields=[
{formatted_fields}
    ]
)

"""

async def main(pool:Pool):
    try:
        # Extraer todas las tablas
        db_tables = await get_all_tables(pool)
        
        all_tables_info = []
        for table in db_tables:
            table_info = await get_fields(table, pool)
            all_tables_info.append(table_info)

        # Crear el archivo con el contenido de todas las tablas
        create_all_migrations_file(all_tables_info)
        
    except asyncpg.exceptions.PostgresError as e:
        return f"Error connecting the db {e}"
    
def create_migration_file(table:dict) -> bool:

    try:
        # Crea una ruta relativa a la carpeta 'generador'
        path = Path("./entities/migrations.py")

        content = migration_file_content(table["table_name"], table["pk"], table["fields"])

        file = create_file(path, content)

    except PermissionError:
        print("Error: No tienes permisos para escribir en este directorio.")
        return False
    except OSError as e:
        print(f"Ocurrió un error del sistema operativo: {e}")
        return False
        

    return file

def create_file(path:Path, content:str):
    
    with open(path, "w") as file:
        file.write(content)