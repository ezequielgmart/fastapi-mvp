# import pytest
# from pygem.main import DBManager, create_db_pool, clean_table
# from .test_db import CONFIG
# from entities.migrations import _authors_gem, _books_gem, _genres_gem, _users_gem
# from asyncpg.pool import Pool
# from asyncpg.exceptions import UniqueViolationError
# import asyncio

# @pytest.mark.asyncio
# async def test_create():
#     pool = await create_db_pool(CONFIG)
#     manager = DBManager(_authors_gem, pool)
    
#     # Define todas las tablas que necesitas limpiar
#     tables = [
#         _authors_gem.get_table(),
#         _books_gem.get_table(),
#         _genres_gem.get_table(),
#         _users_gem.get_table(),
#     ]

#     try:
#         # --- Lógica de la prueba ---
        
#         # Limpieza inicial
#         for table in tables:
#             await clean_table(table, pool)
        
#         # Datos a insertar
#         data = {
#             "author_id": "adsasfasdasdasdasd", 
#             "first_name": "Juan", 
#             "last_name": "Bosch", 
#             "nationality": "Dominican"
#         }
        
#         # Inserción y validación
#         created_author = await manager.create(data)
#         assert created_author is not None
#         assert created_author["author_id"] == data["author_id"]
        
#         # Aquí puedes agregar más lógica de prueba...

#     except Exception as e:
#         # Si algo falla en el 'try', este bloque puede manejarlo.
#         # Es buena práctica relanzar la excepción para que el test marque un fallo.
#         raise e
    
#     finally:
#         # --- Limpieza final ---
#         # Este bloque se ejecuta SIEMPRE, incluso si el test falla.
#         for table in tables:
#             await clean_table(table, pool)
#         await pool.close()


# @pytest.mark.asyncio
# async def test_create_several():

#     pool = await create_db_pool(CONFIG)
#     manager = DBManager(_authors_gem, pool)
    
#     # Define todas las tablas que necesitas limpiar
#     tables = [
#         _authors_gem.get_table(),
#         _books_gem.get_table(),
#         _genres_gem.get_table(),
#         _users_gem.get_table(),
#     ]

#     try:
#         manager = DBManager(_authors_gem, pool)
#         list_of_items = [
#             {"author_id": "dgasdawsdqwdqw", 
#             "first_name": "Francisco", 
#             "last_name":"Pizarro", 
#             "nationality":"British"},
#             {"author_id": "asfxczxca", 
#             "first_name": "Adolft", 
#             "last_name":"Hitler", 
#             "nationality":"French"},
#             {"author_id": "zxcvascasc", 
#             "first_name": "Gabriel", 
#             "last_name":"Marquez", 
#             "nationality":"Dominican"}
#             ]
        
#         # Ejecuta todas las inserciones de forma concurrente
#         insertion_tasks = [manager.create(data) for data in list_of_items]
#         await asyncio.gather(*insertion_tasks)

#         all_authors = await manager.get_all()

#         assert len(all_authors) == len(list_of_items)

#     except Exception as e:
#         # Si algo falla en el 'try', este bloque puede manejarlo.
#         # Es buena práctica relanzar la excepción para que el test marque un fallo.
#         raise e
    
#     finally:
#         # --- Limpieza final ---
#         # Este bloque se ejecuta SIEMPRE, incluso si el test falla.
#         for table in tables:
#             await clean_table(table, pool)
#         await pool.close()
   
    
# @pytest.mark.asyncio
# async def test_create_several():    

#     pool = await create_db_pool(CONFIG)
#     manager = DBManager(_authors_gem, pool)
    
#     # Define todas las tablas que necesitas limpiar
#     tables = [
#         _authors_gem.get_table(),
#         _books_gem.get_table(),
#         _genres_gem.get_table(),
#         _users_gem.get_table(),
#     ]

#     try:
#         manager = DBManager(_authors_gem, pool)
#         list_of_items = [
#             {"author_id": "dgasdawsdqwdqw", 
#             "first_name": "Francisco", 
#             "last_name":"Pizarro", 
#             "nationality":"British"},
#             {"author_id": "asfxczxca", 
#             "first_name": "Adolft", 
#             "last_name":"Hitler", 
#             "nationality":"French"},
#             {"author_id": "zxcvascasc", 
#             "first_name": "Gabriel", 
#             "last_name":"Marquez", 
#             "nationality":"Dominican"}
#             ]
        
#         # Ejecuta todas las inserciones de forma concurrente
#         insertion_tasks = [manager.create(data) for data in list_of_items]
#         await asyncio.gather(*insertion_tasks)

#     except Exception as e:
#             # Si algo falla en el 'try', este bloque puede manejarlo.
#             # Es buena práctica relanzar la excepción para que el test marque un fallo.
#             raise e
        
#     finally:
#         # --- Limpieza final ---
#         # Este bloque se ejecuta SIEMPRE, incluso si el test falla.
#         for table in tables:
#             await clean_table(table, pool)
#         await pool.close()
# # @pytest.mark.asyncio
# # # here probare todo lo relacionado a get_all, get_by_principal_key
# # async def test_gets():

# #     pool = await create_db_pool(CONFIG)

# #     # pytest sabe que debe usar el fixture 'test_db_pool'
# #     # y 'clean_database' se ejecuta automáticamente
# #     manager = DBManager(_authors_gem, pool)

# #     data = {"author_id": "adsasfasdasdasdasd", 
# #             "first_name": "Juan", 
# #             "last_name":"Bosch", 
# #             "nationality":"Dominican"}
    
# #     created_author = await manager.create(data)

# #     assert created_author is not None
# #     assert created_author["author_id"] == data["author_id"]
# #     assert created_author["first_name"] == data["first_name"]
# #     assert created_author["last_name"] == data["last_name"]
# #     assert created_author["nationality"] == data["nationality"]
    

# #     with pytest.raises(UniqueViolationError):
# #         await manager.create(data)


# @pytest.mark.asyncio
# # here probare todo lo relacionado a get_all, get_by_principal_key
# async def test_end():
    
#     pool = await create_db_pool(CONFIG)

#     authors_table = _authors_gem.get_table()
#     books_table = _books_gem.get_table()
#     genres_table = _genres_gem.get_table()
#     users_table = _users_gem.get_table()

#     # limpiarla al final
#     await clean_table(authors_table,pool)
#     await clean_table(books_table,pool)
#     await clean_table(genres_table,pool)
#     await clean_table(users_table,pool)