from pygem.data import SingleGenericSchema
from pygem.pydantic_models import Field


_users_gem = SingleGenericSchema(
    table='users',
    primary_key='user_id',
    fields=[
        Field(is_primary_key=True, name='user_id', type='varchar', is_null=False),
        Field(is_primary_key=False, name='username', type='varchar', is_null=False),
        Field(is_primary_key=False, name='password', type='varchar', is_null=False)
    ]
)


_authors_gem = SingleGenericSchema(
    table='authors',
    primary_key='author_id',
    fields=[
        Field(is_primary_key=True, name='author_id', type='varchar', is_null=False),
        Field(is_primary_key=False, name='first_name', type='varchar', is_null=False),
        Field(is_primary_key=False, name='last_name', type='varchar', is_null=False),
        Field(is_primary_key=False, name='nationality', type='varchar', is_null=True)
    ]
)


_book_authors_gem = SingleGenericSchema(
    table='book_authors',
    primary_key='book_id',
    fields=[
        Field(is_primary_key=True, name='author_id', type='varchar', is_null=False),
        Field(is_primary_key=True, name='book_id', type='varchar', is_null=False),
        Field(is_primary_key=False, name='author_role', type='varchar', is_null=True)
    ]
)


_books_gem = SingleGenericSchema(
    table='books',
    primary_key='book_id',
    fields=[
        Field(is_primary_key=True, name='book_id', type='varchar', is_null=False),
        Field(is_primary_key=False, name='title', type='varchar', is_null=False),
        Field(is_primary_key=False, name='release_date', type='date', is_null=True)
    ]
)


_genres_gem = SingleGenericSchema(
    table='genres',
    primary_key='genre_id',
    fields=[
        Field(is_primary_key=True, name='genre_id', type='integer', is_null=False),
        Field(is_primary_key=False, name='genre_name', type='varchar', is_null=False)
    ]
)


_book_genres_gem = SingleGenericSchema(
    table='book_genres',
    primary_key='book_id',
    fields=[
        Field(is_primary_key=True, name='genre_id', type='integer', is_null=False),
        Field(is_primary_key=True, name='book_id', type='varchar', is_null=False)
    ]
)

