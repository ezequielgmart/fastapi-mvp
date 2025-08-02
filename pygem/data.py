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


"""
"""

* responsabilidades

definir los schemas
generar consultas para una sola tabla 
"""
# representacion de la base de datos y su informacion, asi como acceder a ellos
class Schema: 
    pass 

# generacion de SQL apartir de la base de datos
class SingleQueries(Schema):
    def __init__(schemaObj):
        super().__init__() 

# class SingleEntityModel(SingleQueries):
#     pass 

# insertar esos sql a la base de datos 
class SingleGenericSchema(SingleQueries):
    def __init__(self, table, primary_key, fields):
        self.table = table
        self.primary_key = primary_key
        self.fields = fields