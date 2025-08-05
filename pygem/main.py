# si quiero hacer un pquete debo de poenrle un file main a dodne estaran todas las clases 
"""
Aqui debe de ir todo lo relacionado a lo que hare para traer de nodejs esta herramienta a py

"""

"""

componentes

* Schema: objeto que le pasare al modelo con toda la informacion, en lugar de utilizar un diccionario

* Model: representar en datos la composicion de la tabla relacionada al modelo asi como las funciones para obtener su informacion como main_key, etc

* queries: apartir del schema (composicion de la tabla y su informacion) generar los queries genericos como insert, select, etc. 

    // todo en este componente : 
        Creo que deberia hacerle una opcion a los campos para privatizarlos en el caso de que sea un dato como uan contraseña que no te interesa devolver etc.

* db_client: aqui debo de introducir los queries y ejecutarlos, para luego devolver el resultado. De aqui debe de beber el repositorio;    

Arquitectura: 

* En migrations.py se encarga de la definición de datos.
* La clase Schema se encarga de la representación del esquema.
* La clase SingleQueries se encarga de la generación de consultas.
* La clase DBManager se encarga de la ejecución de consultas.

definir los schemas
generar consultas para una sola tabla 
"""
# La clase Schema ahora es la base, con un constructor que inicializa sus atributos
class Schema:
    def __init__(self, table: str, primary_key: str, fields: list):
        self.table = table
        self.primary_key = primary_key
        self.fields = fields

    def get_table(self) -> str:
        return self.table

    def get_main_key(self) -> str:
        return self.primary_key

    def get_alias(self) -> str:
        return self.table
    
    def get_all_table_fields(self) -> list[str]:
        return [field.name for field in self.fields]

    def convert_fields_to_string(self, fields: list[str]) -> str:
        return ', '.join(fields)

    def get_query_params_for_insert(self) -> list[str]:
        return [f"${i + 1}" for i in range(len(self.fields))]

    def get_query_params_for_update(self) -> list[str]:
        fields_to_set = []
        param_index = 2
        for field in self.fields:
            if not field.is_primary_key:
                fields_to_set.append(f"{field.name} = ${param_index}")
                param_index += 1
        return fields_to_set

# ---
# SingleQueries ahora usa COMPOSICIÓN en lugar de herencia, lo que es mejor
# para desacoplar las responsabilidades.
class SingleQueries:
    def __init__(self, schema: Schema):
        self.schema = schema

    def select_query(self) -> str:
        all_fields = self.schema.get_all_table_fields()
        all_fields_str = self.schema.convert_fields_to_string(all_fields)
        return f"SELECT {all_fields_str} FROM {self.schema.get_table()}"

    def select_query_with_key(self) -> str:
        all_fields = self.schema.get_all_table_fields()
        all_fields_str = self.schema.convert_fields_to_string(all_fields)
        return f"SELECT {all_fields_str} FROM {self.schema.get_table()} WHERE {self.schema.get_main_key()} = $1"

    def insert_query(self) -> str:
        table_fields = self.schema.get_all_table_fields()
        table_fields_str = self.schema.convert_fields_to_string(table_fields)
        
        query_params = self.schema.get_query_params_for_insert()
        query_params_str = self.schema.convert_fields_to_string(query_params)
        
        return f"INSERT INTO {self.schema.get_table()} ({table_fields_str}) VALUES ({query_params_str}) RETURNING {table_fields_str}"

    def update_query(self) -> str:
        all_fields_str = self.schema.convert_fields_to_string(self.schema.get_all_table_fields())
        query_params_for_update = self.schema.get_query_params_for_update()
        query_params_for_update_str = self.schema.convert_fields_to_string(query_params_for_update)
        
        return f"UPDATE {self.schema.get_table()} SET {query_params_for_update_str} WHERE {self.schema.get_main_key()} = $1 RETURNING {all_fields_str}"

    def delete_query(self) -> str:
        return f"DELETE FROM {self.schema.get_table()} WHERE {self.schema.get_main_key()} = $1"


# ---
# SingleGenericSchema hereda de Schema, ya no de SingleQueries.
# Esto asegura que SingleGenericSchema es un objeto de tipo Schema.
class SingleGenericSchema(Schema):
    def __init__(self, table: str, primary_key: str, fields: list):
        super().__init__(table, primary_key, fields)
        self.queries = SingleQueries(self) # <-- Crea el objeto de consultas aquí


# OJO deberia de haber una clase para las funciones de lidiar con la bdd para aislar los datos de la bdd de las querys y la generacion de esas porque de esa manera puedo tener aisaldo la bdd y porbarala en entorno de pruebas pasandole la getpool por parametro como una inyeccion de dependencia        
# ---
# DBManager ahora es funcional y usa la inyección de dependencias.
class DBManager:
    def __init__(self, schema_entity: SingleGenericSchema, get_db_pool):
        self.schema_entity = schema_entity
        self.get_db_pool = get_db_pool

    async def _query_with_params(self, query_text: str, query_params: list) -> list:
        pool = await self.get_db_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(query_text, *query_params)
    
    async def single_query(self, query_text: str) -> list:
        pool = await self.get_db_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(query_text)