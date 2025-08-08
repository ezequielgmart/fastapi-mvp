# # probar las queries generadas dinamicamente: 
# from pygem.main import *
# from pygem.pydantic_models import Field
# from entities.migrations import _authors_gem,_users_gem,_books_gem,_genres_gem

# def test_select_query():
  
#     first_result = _authors_gem.queries.select_query()
#     second_result = _users_gem.queries.select_query()
#     third_result = _books_gem.queries.select_query()
#     fourth_result = _genres_gem.queries.select_query()

#     assert first_result == "SELECT author_id, first_name, last_name, nationality FROM authors"
#     assert second_result == "SELECT user_id, username, password FROM users"
#     assert third_result == "SELECT book_id, title, release_date FROM books"
#     assert fourth_result == "SELECT genre_id, genre_name FROM genres"

# def test_select_query_with_principal_key():

#     query_result = _authors_gem.queries.select_query_with_principal_key()
#     assert query_result == "SELECT author_id, first_name, last_name, nationality FROM authors WHERE author_id = $1"

# def test_select_query_with_key():
#     key = "first_name"
    
#     query_result = _authors_gem.queries.select_query_with_key(key)
#     assert query_result == f"SELECT author_id, first_name, last_name, nationality FROM authors WHERE {key} = $1"

# def test_insert_query():
    
#     query_result = _authors_gem.queries.insert_query()
#     assert query_result == f"INSERT INTO authors (author_id, first_name, last_name, nationality) VALUES ($1, $2, $3, $4) RETURNING author_id, first_name, last_name, nationality"

# def test_update_query():
    
#     # expected_result = _authors_gem.queries.update_query()
#     expected_result = _authors_gem.queries.update_query()

#     assert expected_result == f"UPDATE authors SET first_name = $2, last_name = $3, nationality = $4 WHERE author_id = $1 RETURNING author_id, first_name, last_name, nationality"

# def test_delete_query():
    
#     query_result = _authors_gem.queries.delete_query()
#     assert query_result == f"DELETE FROM authors WHERE author_id = $1"
