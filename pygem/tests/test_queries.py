# probar las queries generadas dinamicamente: 

from pygem.main import *
from pygem.pydantic_models import Field
# from entities.migrations import _authors_gem



def test_select_query():
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
    query_result = _authors_gem.queries.select_query()
    assert query_result == "SELECT author_id, first_name, last_name, nationality FROM authors"
