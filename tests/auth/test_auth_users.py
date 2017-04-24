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

def test_create_user_sync(test_project, waf):
    """Test creating a user from engine."""
    engine = get_engine('default')
    users.create_user_sync(engine, username='test2', password='pass2')
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test2')
        row = [r for r in con.execute(query)][0]
        assert users.check_password('pass2', row.password)

def test_check_password_returns_false_on_mismatch():
    """Test password check when the passwords don't match."""
    encoded = users.make_password('test_pass')
    assert users.check_password('test_what', encoded) == False

@pytest.mark.asyncio
async def test_check_user_reset_access_split_token(test_project, waf):
    await waf.create_database_pool('default')
    async with Connection() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test')
        row = await con.fetchrow(query)
        user_id = row.id
    token = await users.generate_reset_split_token(user_id)
    verified = await users.check_user_reset_access('test', user_id, token)
    assert verified
    await waf.close_database_pools()

@pytest.mark.asyncio
async def test_check_user_reset_access_split_token_bad_token(test_project, waf):
    await waf.create_database_pool('default')
    async with Connection() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test')
        row = await con.fetchrow(query)
        user_id = row.id
    token = await users.generate_reset_split_token(user_id)
    verified = await users.check_user_reset_access('test', user_id, 'whatever')
    assert not verified
    await waf.close_database_pools()

@pytest.mark.asyncio
async def test_check_user_reset_access_split_token_bad_user_id(test_project, waf):
    await waf.create_database_pool('default')
    async with Connection() as con:
        query = sa.select('*').select_from(tables.user)
        row = await con.fetchrow(query)
        user_id = row.id
    token = await users.generate_reset_split_token(user_id)
    verified = await users.check_user_reset_access('test', 3, 'whatever')
    assert not verified
    await waf.close_database_pools()

@pytest.mark.asyncio
async def test_generate_password_reset_path(test_project, waf):
    await waf.create_database_pool('default')
    async with Connection() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username=='test')
        row = await con.fetchrow(query)
        user_id = row.id
    url = await users.generate_password_reset_path(user_id)
    assert '/auth/password_reset/' in url
    await waf.close_database_pools()
