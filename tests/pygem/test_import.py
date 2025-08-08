# import pytest
# from pygem.imports import *
# from pygem.main import create_db_pool
# from .test_db import CONFIG
# from pygem.pydantic_models import Field

# from pathlib import Path

# # Corrección en test_import.py


# @pytest.mark.asyncio
# async def test_main():

#     pool = await create_db_pool(CONFIG)

#     try:
#         # conn = await db.start_connection(CONFIG)
#         await main(pool)

#         # comprueba que el archivo resultante sea u narchivo valido
#         result_path = Path("./entities/migrations.py")
#         assert result_path.is_file()
        
#         # archivo para comprobar 
#         test_path = Path("./pygem/test_file_migrations.py")


#         with open(result_path, "r") as file:
#             result_file_content = file.read()
            

#         with open(test_path, "r") as file:
#             test_file_content = file.read()

#         assert result_file_content.strip() == test_file_content.strip()

#     finally:
#         await pool.close()
#         # result_path.unlink()
    
# @pytest.mark.asyncio
# async def test_all_tables():
    
#     pool = await create_db_pool(CONFIG)

#     try:
    
#         expected_tables = ["users",
#         "authors",
#         "book_authors",
#         "books",
#         "genres",
#         "book_genres"]
        
#         # conn = await db.start_connection(CONFIG)
        
#         result = await get_all_tables(pool)

#         assert result == expected_tables

    
#     finally:
#         await pool.close()
  

    
# # Corrección de tu test_get_fields_tables
# @pytest.mark.asyncio
# async def test_get_fields_tables():
    
#     pool = await create_db_pool(CONFIG)

#     try:
#         # conn = await db.start_connection(CONFIG)
#         table = "authors"
        
#         table_info = await get_fields(table, pool)
        
#         # Simula los datos y crea los objetos Field esperados
#         fields_data = [
#             {'is_primary_key': True, 'name': 'author_id', 'type': 'varchar', 'is_null': False},
#             {'is_primary_key': False, 'name': 'first_name', 'type': 'varchar', 'is_null': False},
#             {'is_primary_key': False, 'name': 'last_name', 'type': 'varchar', 'is_null': False},
#             {'is_primary_key': False, 'name': 'nationality', 'type': 'varchar', 'is_null': True},
#         ]
#         expected_fields_objects = [Field(**data) for data in fields_data]
        
#         # Construye el diccionario esperado con la misma estructura que get_fields()
#         expected_table_info = {
#             "table_name": "authors",
#             "pk": "author_id",
#             "fields": expected_fields_objects
#         }
        
#         # Ahora la aserción compara un diccionario con otro diccionario
#         assert table_info == expected_table_info
        
#     finally:
#         await pool.close()



