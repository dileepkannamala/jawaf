import pytest
import asyncpgsa.connection
from jawaf.db import Connection, create_tables, get_engine
    
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

@pytest.mark.asyncio
async def test_connection(test_project, waf):
    """Test the Connection class."""
    await waf.create_database_pool('default')
    async with Connection() as con:
        assert type(con) == asyncpgsa.connection.SAConnection
    await waf.close_database_pools()