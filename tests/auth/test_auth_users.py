import pytest
import sqlalchemy as sa
from jawaf.auth import tables, users
from jawaf.db import Connection, get_engine
    
@pytest.mark.asyncio
async def test_create_user(test_project, waf):
    """Test creating a user."""
    await waf.create_database_pool('default')
    await users.create_user(username='test', password='pass')
    async with Connection() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test')
        row = await con.fetchrow(query)
    assert users.check_password('pass', row.password)
    await waf.close_database_pools()

def test_create_user_from_engine(test_project, waf):
    """Test creating a user from engine."""
    engine = get_engine('default')
    users.create_user_from_engine(engine, username='test2', password='pass2')
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test2')
        row = [r for r in con.execute(query)][0]
        assert users.check_password('pass2', row.password)

def test_check_password_returns_false_on_mismatch():
    """Test password check when the passwords don't match."""
    encoded = users.make_password('test_pass')
    assert users.check_password('test_what', encoded) == False