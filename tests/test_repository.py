# import pytest
# from pygem.main import GemRepository
# from config.connect import CONFIG, DbPool, create_db_pool 
# from entities.migrations import _authors_gem
# from entities.author import Author



# class AuthorTestGem(GemRepository):
#     def __init__(self, pool: DbPool):
#         self.gem = _authors_gem
#         super().__init__(model=Author, gem=self.gem, pool=pool)
     
# # # # here probare todo lo relacionado a get_all, get_by_principal_key
# @pytest.mark.asyncio
# async def test_gets():
#     pool = await create_db_pool(CONFIG)
#     test_author = AuthorTestGem(pool) 

#     result = await test_author.get_all()
#     assert len(result) == 3  

# @pytest.mark.asyncio
# async def test_get_by_id():
    
#     pool = await create_db_pool(CONFIG)

#     id = "2cf1b3cf-2c2e-4889-a57b-cfc3a653ad31"
#     test_author = AuthorTestGem(pool) 

#     result = await test_author.get_by_id(id)

#     assert result.author_id == id


# @pytest.mark.asyncio
# async def test_update():
    
#     pool = await create_db_pool(CONFIG)
#     id = "8abb6077-ed99-4915-a957-614474531c62"

#     author = {
#             "author_id":"8abb6077-ed99-4915-a957-614474531c62",
#             "first_name":"Erwin",
#             "last_name":"Rommel",
#             "nationality":"Austrian",
#     }
        
    
#     test_author = AuthorTestGem(pool) 
    
#     data_to_insert = Author(**author)
#     result = await test_author.update(id, data_to_insert)
    

#     assert test_author.gem.queries.update_query() == id
#     assert result.author_id == id


# @pytest.mark.asyncio
# async def test_create():
    
#     pool = await create_db_pool(CONFIG)

#     author = {
#             "author_id":str(uuid.uuid4()),
#             "first_name":"Adolf",
#             "last_name":"Hitler",
#             "nationality":"Austrian",
#         }
        
    
#     test_author = AuthorTestGem(pool) 
    
#     result = await test_author.create(Author(**author))
    

#     assert result.author_id == id