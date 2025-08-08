import asyncio
import asyncpg
from asyncpg.pool import Pool
from typing import TypeVar, List, Dict, Any
from pydantic import BaseModel


class Field(BaseModel):
    is_primary_key:bool
    name:str
    type:str
    is_null:bool
    name:str


"""
@function: Creates and returns a database connection pool.
@params: 
    - config: A dictionary with the database connection information.
@return: A Pool object.
"""
async def create_db_pool(config) -> Pool:
    """Creates and returns a database connection pool."""
    pool = await asyncpg.create_pool(
        min_size=1,     # Minimum number of open connections
        max_size=10,    # Maximum number of connections
        loop=None,
        **config
    )
    return pool

"""
@function: Deletes all records from a given table.
@params: 
    - table: The name of the table to clean.
    - pool: The database connection pool.
@return: None
"""
async def clean_table(table, pool): 
    async with pool.acquire() as conn:
        await conn.execute(f"DELETE FROM {table}")


"""
@class: Represents the schema of a database table.
@params: 
    - table: The name of the table.
    - primary_key: The name of the primary key.
    - fields: A list of Field objects that describe the table's fields.
@return: An instance of the Schema class.
"""
class Schema:
    """
    @method: Initializes the table schema.
    @params:
        - table: The name of the table.
        - primary_key: The name of the primary key.
        - fields: A list of Field objects that describe the table's fields.
    @return: None
    """
    def __init__(self, table: str, primary_key: str, fields: list):
        self.table = table
        self.primary_key = primary_key
        self.fields = fields

    """
    @method: Gets the name of the table.
    @params: None
    @return: The table name as a string.
    """
    def get_table(self) -> str:
        return self.table

    """
    @method: Gets the name of the primary key.
    @params: None
    @return: The primary key name as a string.
    """
    def get_main_key(self) -> str:
        return self.primary_key

    """
    @method: Gets the table's alias (in this case, the same name).
    @params: None
    @return: The table alias as a string.
    """
    def get_alias(self) -> str:
        return self.table
    
    """
    @method: Gets a list of the names of all table fields.
    @params: None
    @return: A list of strings with the field names.
    """
    def get_all_table_fields(self) -> list[str]:
        return [field.name for field in self.fields]

    """
    @method: Converts a list of fields into a comma-separated string.
    @params: 
        - fields: A list of strings with the field names.
    @return: A string with the fields joined by commas.
    """
    def convert_fields_to_string(self, fields: list[str]) -> str:
        return ', '.join(fields)

    """
    @method: Generates a list of placeholders for an insert query ($1, $2, etc.).
    @params: None
    @return: A list of strings with the placeholders.
    """
    def get_query_params_for_insert(self) -> list[str]:
        return [f"${i + 1}" for i in range(len(self.fields))]

    """
    @method: Generates a list of field assignments for an update query.
    @params: None
    @return: A list of strings in the format 'field = $N'.
    """
    def get_query_params_for_update(self) -> list[str]:
        fields_to_set = []
        param_index = 2
        for field in self.fields:
            if not field.is_primary_key:
                fields_to_set.append(f"{field.name} = ${param_index}")
                param_index += 1
        return fields_to_set

# ---
"""
@class: Generates generic SQL queries for a single table.
@params:
    - schema: An instance of the Schema class.
@return: An instance of the SingleQueries class.
"""
class SingleQueries:
    """
    @method: Initializes the query generator class with a schema.
    @params:
        - schema: An instance of the Schema class.
    @return: None
    """
    def __init__(self, schema: Schema):
        self.schema = schema

    """
    @method: Generates an SQL query to select all records from the table.
    @params: None
    @return: A string with the SQL query.
    """
    def select_query(self) -> str:
        all_fields = self.schema.get_all_table_fields()
        all_fields_str = self.schema.convert_fields_to_string(all_fields)
        return f"SELECT {all_fields_str} FROM {self.schema.get_table()}"

    """
    @method: Generates an SQL query to select a record by its primary key.
    @params: None
    @return: A string with the SQL query.
    """
    def select_query_with_principal_key(self) -> str:
        all_fields = self.schema.get_all_table_fields()
        all_fields_str = self.schema.convert_fields_to_string(all_fields)
        return f"SELECT {all_fields_str} FROM {self.schema.get_table()} WHERE {self.schema.get_main_key()} = $1"
    
    """
    @method: Generates an SQL query to select a record by a given key.
    @params: 
        - key: The name of the key to filter by.
    @return: A string with the SQL query.
    """
    def select_query_with_key(self, key) -> str:
        all_fields = self.schema.get_all_table_fields()
        all_fields_str = self.schema.convert_fields_to_string(all_fields)
        return f"SELECT {all_fields_str} FROM {self.schema.get_table()} WHERE {key} = $1"
    
    """
    @method: Generates an SQL query to insert a new record.
    @params: None
    @return: A string with the SQL query.
    """
    def insert_query(self) -> str:
        table_fields = self.schema.get_all_table_fields()
        table_fields_str = self.schema.convert_fields_to_string(table_fields)
        
        query_params = self.schema.get_query_params_for_insert()
        query_params_str = self.schema.convert_fields_to_string(query_params)
        
        return f"INSERT INTO {self.schema.get_table()} ({table_fields_str}) VALUES ({query_params_str}) RETURNING {table_fields_str}"

    """
    @method: Generates an SQL query to update a record.
    @params: None
    @return: A string with the SQL query.
    """
    def update_query(self) -> str:
        all_fields_str = self.schema.convert_fields_to_string(self.schema.get_all_table_fields())
        query_params_for_update = self.schema.get_query_params_for_update()
        query_params_for_update_str = self.schema.convert_fields_to_string(query_params_for_update)
        
        return f"UPDATE {self.schema.get_table()} SET {query_params_for_update_str} WHERE {self.schema.get_main_key()} = $1 RETURNING {all_fields_str}"

    """
    @method: Generates an SQL query to delete a record.
    @params: None
    @return: A string with the SQL query.
    """
    def delete_query(self) -> str:
        all_fields_str = self.schema.convert_fields_to_string(self.schema.get_all_table_fields())
        return f"DELETE FROM {self.schema.get_table()} WHERE {self.schema.get_main_key()} = $1 RETURNING {all_fields_str}"


# ---
"""
@class: Represents a generic single-table schema.
@params:
    - table: The name of the table.
    - primary_key: The name of the primary key.
    - fields: A list of Field objects that describe the table's fields.
@return: An instance of the SingleGenericSchema class.
"""
class SingleGenericSchema(Schema):
    """
    @method: Initializes the schema and the query generator.
    @params:
        - table: The name of the table.
        - primary_key: The name of the primary key.
        - fields: A list of Field objects that describe the table's fields.
    @return: None
    """
    def __init__(self, table: str, primary_key: str, fields: list):
        super().__init__(table, primary_key, fields)
        self.queries = SingleQueries(self) 

# ---
T = TypeVar('T', bound=BaseModel)

"""
@class: Manages database interaction using asyncpg.
@params:
    - schema_entity: An instance of SingleGenericSchema.
    - pool: The database connection pool.
@return: An instance of the DBManager class.
"""
class DBManager:
    """
    @method: Initializes the database manager.
    @params:
        - schema_entity: An instance of SingleGenericSchema.
        - pool: The database connection pool.
    @return: None
    """
    def __init__(self, schema_entity: SingleGenericSchema, pool: Pool):
        self.schema_entity = schema_entity
        self.pool = pool
        
    """
    @method: Gets all records from the table.
    @params: None
    @return: A list of dictionaries with the database records.
    """
    async def get_all(self) -> List[Dict[str, Any]]:
        query = self.schema_entity.queries.select_query()
        async with self.pool.acquire() as conn:
            records = await conn.fetch(query)
            return [dict(record) for record in records]
    
    """
    @method: Gets a single record by its primary key.
    @params: 
        - key_value: The primary key value of the record to find.
    @return: A dictionary with the record or None if not found.
    """
    async def get_by_principal_key(self, key_value) -> Dict[str, Any] | None:
        query = self.schema_entity.queries.select_query_with_principal_key()
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(query, key_value)
            return dict(record) if record else None
    
    """
    @method: Creates a new record in the database.
    @params:
        - data: A dictionary with the data for the new record.
    @return: A dictionary with the created record or None if the operation fails.
    """
    async def create(self, data: dict) -> Dict[str, Any] | None:
        insert_query = self.schema_entity.queries.insert_query()
        values = [data.get(field.name) for field in self.schema_entity.fields]

        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(insert_query, *values)
            return dict(record) if record else None

    """
    @method: Updates a record by its primary key.
    @params:
        - key_value: The primary key value of the record to update.
        - data: A dictionary with the data to update.
    @return: A dictionary with the updated record or None if not found.
    """
    async def update(self, key_value, data: dict) -> Dict[str, Any] | None:
        update_query = self.schema_entity.queries.update_query()
        
        update_fields = [field for field in self.schema_entity.fields if not field.is_primary_key]
        update_values = [data.get(field.name) for field in update_fields]
        
        # Fixed: The key_value must come first to match the SQL query's parameter order.
        params = [key_value] + update_values
        
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(update_query, *params)
            return dict(record) if record else None

    """
    @method: Deletes a record by its primary key.
    @params:
        - key_value: The primary key value of the record to delete.
    @return: A dictionary with the deleted record or None if not found.
    """
    async def delete(self, key_value) -> Dict[str, Any] | None:
        delete_query = self.schema_entity.queries.delete_query()
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(delete_query, key_value)
            return dict(record) if record else None


"""
@class: A generic base class for repositories, adaptable to any Pydantic model.
@params:
    - model: The Pydantic model for the repository.
    - gem: The generic table schema.
    - pool: The database connection pool.
@return: An instance of the GemRepository class.
"""
class GemRepository:
    """
    @method: Initializes the repository with the model, schema (gem), and connection pool.
    @params:
        - model: The Pydantic model for the repository.
        - gem: The generic table schema.
        - pool: The database connection pool.
    @return: None
    """
    def __init__(self, model: T, gem: SingleGenericSchema, pool: Pool):
        self.model = model
        self.pool = pool
        self.gem = gem
        self.manager = DBManager(self.gem, self.pool)

    """
    @method: Gets all records and converts them to a list of model objects.
    @params: None
    @return: A list of T model objects.
    """
    async def get_all(self) -> List[T]:
        db_data = await self.manager.get_all()
        return [self.model(**data) for data in db_data]
    
    """
    @method: Gets a record by its primary key and converts it to a model object.
    @params: 
        - key_value: The primary key value.
    @return: A T model object or None if not found.
    """
    async def get_by_id(self, key_value) -> T | None:
        db_data = await self.manager.get_by_principal_key(key_value)
        if db_data:
            return self.model(**db_data)
        return None
    
    """
    @method: Creates a new record and converts it to a model object.
    @params:
        - data: A T model object with the data to create.
    @return: A created T model object or None if the operation fails.
    """
    async def create(self, data: T) -> T | None:
        db_data = await self.manager.create(data.model_dump())
        if db_data:
            return self.model(**db_data)
        return None

    """
    @method: Updates a record and converts it to a model object.
    @params:
        - key_value: The primary key value of the record to update.
        - data: A T model object with the data to update.
    @return: An updated T model object or None if not found.
    """
    async def update(self, key_value, data: T) -> T | None:
        db_data = await self.manager.update(key_value, data.model_dump())
        if db_data:
            # Fixed: Return the full object so the test can pass.
            return self.model(**db_data)
        return None
        
    """
    @method: Deletes a record and converts it to a model object.
    @params:
        - key_value: The primary key value of the record to delete.
    @return: A deleted T model object or None if not found.
    """
    async def delete(self, key_value) -> T | None:
        db_data = await self.manager.delete(key_value)
        if db_data:
            return self.model(**db_data)
        return None