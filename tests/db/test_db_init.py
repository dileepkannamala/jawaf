import pytest
import asyncpgsa.connection
from jawaf.db import Connection, create_tables, get_engine, get_metadata
    
@pytest.mark.asyncio
async def test_create_tables(test_project, waf):
    """Test create tables command creates the table from the test app."""
    create_tables(['test_app'], warn=False)
    await waf.create_database_pool('default')
    async with Connection() as con:
        await con.execute("INSERT INTO test_app_person VALUES (1, 'test_1')")
        row = await con.fetchrow('''SELECT * FROM test_app_person''')
        assert row.id == 1
    await waf.close_database_pools()

def test_get_metadata(test_project, waf):
    """Test get_metadata"""
    from jawaf.conf import settings
    metadata_list = get_metadata(settings.INSTALLED_APPS)
    from jawaf.auth.tables import metadata
    assert metadata in metadata_list

@pytest.mark.asyncio
async def test_connection(test_project, waf):
    """Test the Connection class."""
    await waf.create_database_pool('default')
    async with Connection() as con:
        assert type(con) == asyncpgsa.connection.SAConnection
    await waf.close_database_pools()