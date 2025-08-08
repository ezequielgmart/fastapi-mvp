# # tests/test_authors.py

# import pytest
# import asyncio
# from fastapi.testclient import TestClient
# from main import app
# from config.db import CONFIG, create_db_pool
# from config.connect import DbPool
# from entities.author import Author

# # Creamos una instancia del cliente de prueba
# client = TestClient(app)

# # Datos de prueba con author_id para usar en los tests
# # Se han añadido los IDs para que coincidan con la lógica de inserción
# test_authors_data = [
#     {"author_id": "e99c962c-2ec2-432f-ac76-4f82f129fc54", "first_name": "Gabriel", "last_name": "García Márquez", "nationality": "Colombiana"},
#     {"author_id": "8b93540e-7c15-4a25-a4f5-5601c4484b80", "first_name": "Isabel", "last_name": "Allende", "nationality": "Chilena"},
# ]

# # --- Se ha eliminado el fixture `event_loop` ya que pytest-asyncio lo maneja automáticamente. ---

# @pytest.fixture(scope="session")
# async def db_pool_fixture() -> DbPool:
#     """
#     Fixture para crear un pool de conexiones a la base de datos de prueba.
#     """
#     pool = await create_db_pool(CONFIG)
#     yield pool
#     await pool.close()

# @pytest.fixture(autouse=True)
# async def setup_db(db_pool_fixture: DbPool):
#     """
#     Fixture para configurar y limpiar la base de datos antes y después de cada test.
#     """
#     async with db_pool_fixture.acquire() as conn:
#         # Limpiamos los datos de la tabla 'authors' para asegurar un estado limpio.
#         await conn.execute("DELETE FROM authors")
        
#         # Insertamos los datos de prueba que ahora incluyen el author_id
#         insert_query = """
#         INSERT INTO authors (author_id, first_name, last_name, nationality) 
#         VALUES ($1, $2, $3, $4)
#         """
#         await conn.executemany(insert_query, [
#             (a['author_id'], a['first_name'], a['last_name'], a['nationality'])
#             for a in test_authors_data
#         ])
    
#     # El 'yield' marca el final del setup y el inicio del test.
#     yield

# # --- Todos los tests que usan fixtures asíncronos deben ser `async def`. ---

# async def test_get_authors_success_end_to_end():
#     """
#     Test de extremo a extremo para la ruta GET /authors/.
#     """
#     response = client.get("/authors/")

#     # Verificamos que el código de estado es 200 (OK).
#     assert response.status_code == 200

#     # Verificamos que la respuesta JSON coincide con nuestros datos de prueba.
#     assert response.json() == test_authors_data

# async def test_get_author_by_id_success():
#     """
#     Test para obtener un autor específico por su ID.
#     """
#     # Usamos el ID del primer autor de nuestros datos de prueba para asegurar que existe.
#     first_author_id = test_authors_data[0]["author_id"]
#     response = client.get(f"/authors/{first_author_id}")
    
#     assert response.status_code == 200
#     assert response.json() == test_authors_data[0]

# async def test_get_author_by_id_not_found():
#     """
#     Test para verificar que se devuelve 404 si el autor no existe.
#     """
#     # Usamos un UUID válido que no existe en la base de datos.
#     non_existent_uuid = "12345678-1234-5678-1234-567812345678"
#     response = client.get(f"/authors/{non_existent_uuid}")
    
#     # El código de estado es 404.
#     assert response.status_code == 404
#     # La respuesta JSON debe coincidir exactamente con el mensaje de tu controlador.
#     assert response.json()["detail"] == f"Author with id '{non_existent_uuid}' not found."

# async def test_create_new_author():
#     """
#     Test para crear un nuevo autor.
#     """
#     new_author = {
#         "first_name": "Julio",
#         "last_name": "Cortázar",
#         "nationality": "Argentina"
#     }
    
#     response = client.post("/authors/", json=new_author)
    
#     assert response.status_code == 200
#     created_author = response.json()
#     assert created_author["first_name"] == "Julio"
#     assert created_author["last_name"] == "Cortázar"
#     assert "author_id" in created_author