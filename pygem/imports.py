# This file is for testing the MVP of extracting database information
# and converting it into a manipulable object/class for the Schema class.
# This object should be saved along with all other table schemas
# in a common file called "imports.db" for all instantiated objects to be used.

# extract data from a db
import asyncpg
from asyncpg.pool import Pool
from pathlib import Path
from .pydantic_models import Field
from asyncpg.exceptions import PostgresError


"""
@function: Gets a list of all table names from the 'public' schema.
@params: 
    - pool: An asyncpg connection pool.
@return: A list of strings with table names, or a string with an error message.
"""
async def get_all_tables(pool:Pool) -> list[str]:
    try:
        # Borrow a connection from the pool, it's automatically returned upon exiting the block
        async with pool.acquire() as conn: 
            # 1. Extract all tables from the 'public' schema
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

"""
@function: Gets a table's column information and converts it into a structured dictionary.
@params: 
    - table: The name of the table.
    - pool: An asyncpg connection pool.
@return: A dictionary containing the table's name, primary key, and a list of Field objects.
"""
async def get_fields(table:str, pool:Pool) -> dict[str, Any]:
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
            
            # --- Solution to UnboundLocalError ---
            # Assign a default value to data_type at the beginning of the loop.
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

            # Improved duplicate check
            if not any(f.name == field["name"] for f in fields):
                fields.append(Field(**field))

    result = {"table_name": table, "pk": primary_key_name, "fields": fields}

    return result

"""
@function: Creates a file containing all table schemas in a standard format.
@params: 
    - all_tables_info: A list of dictionaries with table information.
@return: True if the file was created successfully, False otherwise.
"""
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
        print(f"An error occurred while creating the migrations file: {e}")
        return False

"""
@function: Creates the code block for a single table's schema.
@params: 
    - table: The name of the table.
    - primary_key_name: The name of the primary key.
    - fields: A list of Field objects.
@return: A string with the formatted Python code for the table schema.
"""
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

"""
@function: The main function to orchestrate the extraction and file creation process.
@params:
    - pool: An asyncpg connection pool.
@return: A string with an error message if a PostgresError occurs.
"""
async def main(pool:Pool):
    try:
        # Extract all tables
        db_tables = await get_all_tables(pool)
        
        all_tables_info = []
        for table in db_tables:
            table_info = await get_fields(table, pool)
            all_tables_info.append(table_info)

        # Create the file with all the tables' content
        create_all_migrations_file(all_tables_info)
        
    except asyncpg.exceptions.PostgresError as e:
        return f"Error connecting the db {e}"

"""
@function: Creates a single migration file for a given table.
@params:
    - table: A dictionary with the table's information.
@return: True if the file was created successfully, False otherwise.
"""
def create_migration_file(table:dict) -> bool:
    try:
        # Creates a path relative to the 'generator' folder
        path = Path("./entities/migrations.py")

        content = migration_file_content(table["table_name"], table["pk"], table["fields"])

        create_file(path, content)
        return True

    except PermissionError:
        print("Error: You don't have permission to write to this directory.")
        return False
    except OSError as e:
        print(f"An operating system error occurred: {e}")
        return False
        
"""
@function: Creates a file at a given path with the specified content.
@params:
    - path: A Path object for the file location.
    - content: A string with the content to write to the file.
@return: None
"""
def create_file(path:Path, content:str):
    with open(path, "w") as file:
        file.write(content)