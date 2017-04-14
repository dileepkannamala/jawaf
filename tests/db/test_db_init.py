import pytest
import asyncpgsa.connection
from jawaf.db import Connection, create_tables, get_engine
    
@pytest.mark.asyncio
async def test_create_tables(test_project, waf):
    """Test create tables command creates the table from the test app."""
    create_tables(['test_app'], warn=False)
    await waf.create_database_pool('default')
    async with Connection() as con:
        row = await con.fetchrow('''SELECT EXISTS (
           SELECT 1
           FROM   pg_tables
           WHERE  tablename = 'test_app_person');
        ''')
        assert row.exists == True
    await waf.close_database_pools()

@pytest.mark.asyncio
async def test_connection(test_project, waf):
    """Test the Connection class."""
    await waf.create_database_pool('default')
    async with Connection() as con:
        assert type(con) == asyncpgsa.connection.SAConnection
    await waf.close_database_pools()