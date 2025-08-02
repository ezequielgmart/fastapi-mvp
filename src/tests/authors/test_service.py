# from src.features.models.author import Author
# from src.features.authors.service import author_service
# from src.utils.exceptions import EXCEPTIONS
# from config.db import check_db_run
# import pytest

# # main.py o config.py
# import os
# from dotenv import load_dotenv

# """

# """

# # Carga las variables desde el archivo .env
# load_dotenv()

# # Ahora puedes acceder a las variables de entorno con os.environ o os.getenv
# config = {
#     "user":os.getenv("TEST_DB_USER"),
#     "host":os.getenv("TEST_DB_HOST"),
#     "name":os.getenv("TEST_DB_DATABASE"),
#     "password":os.getenv("TEST_DB_PASSWORD"),
# }

# # @pytest.fixture
# def test_get_all():
#     authors = author_service.get_all_authors()
#     assert len(authors) == 3, "result len should be 3"

    
# def test_get_by_id():
#     author = {
#         "author_id": "lkjhgasdfgascnzkquwodanscnzxkcva154",
#         "name": "Juan",
#         "last_name": "Bosh",
#         "nationality": "Dominican"
#     }
     
#     result = author_service.get_by_id(author["author_id"])

#     assert result.author_id == author["author_id"], "both id should be the same"
#     assert result.name == author["name"], "both name should be the same"
#     assert result.last_name == author["last_name"], "both last_name should be the same"
#     assert result.nationality== author["nationality"], "both nationality should be the same"

# def test_insert():

#     author = {
#         "author_id": "asdfganzxkcva154lkjhgscnzkquwodansc",
#         "name": "J.K",
#         "last_name": "Rowlling",
#         "nationality": "British"
#     }

#     # Create an instance of Author model
#     obj_to_insert = Author(**author) 
     
#     result = author_service.insert(obj_to_insert)

#     assert result.author_id == author["author_id"], "both id should be the same"
#     assert result.name == author["name"], "both name should be the same"
#     assert result.last_name == author["last_name"], "both last_name should be the same"
#     assert result.nationality== author["nationality"], "both nationality should be the same"

# def test_insert_duplicate():

#     author = {
#         "author_id": "asdfganzxkcva154lkjhgscnzkquwodansc",
#         "name": "J.K",
#         "last_name": "Rowlling",
#         "nationality": "British"
#     }

#     # Create an instance of Author model
#     obj_to_insert = Author(**author) 
#     with pytest.raises(ValueError, match=f"{EXCEPTIONS["db_duplicated_id"]}"):
#         author_service.insert(obj_to_insert)



# @pytest.mark.asyncio
# async def test_check_db_run():
#     result = await check_db_run(config)
#     assert EXCEPTIONS["db_connected"] in result # def test_insert