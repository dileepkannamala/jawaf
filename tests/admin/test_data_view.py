import pytest
import sqlalchemy as sa
from jawaf.auth import tables, users
from jawaf.db import get_engine

def create_admin_test_user(name):
    """Create test users."""
    engine = get_engine('default')
    users.create_user_from_engine(engine, username=name, password='admin_pass_test')
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username==name)
        row = con.execute(query)
        user_id = row.fetchone().id
    return user_id

def test_data_delete(test_project, waf):
    """Test posting a new user"""
    user_id = create_admin_test_user('admin_test_delete')
    form_data = {
        'id': user_id,
    }
    request, response = waf.server.test_client.delete('/admin/user/', json=form_data, headers=waf.default_headers)
    assert response.status == 200

def test_data_get(test_project, waf):
    """Test posting a new user"""
    user_id = create_admin_test_user('admin_test_get')
    request, response = waf.server.test_client.get('/admin/user/?id=%s' % user_id, headers=waf.default_headers)
    assert response.status == 200

def test_data_post(test_project, waf):
    """Test posting a new user"""
    form_data = {
        'username': 'cool',
        'password': 'cool_pass',
        'is_active': True,
        'is_staff': True,
    }
    request, response = waf.server.test_client.post('/admin/user/', json=form_data, headers=waf.default_headers)
    assert response.status == 201

def test_data_put(test_project, waf):
    """Test posting a new user"""
    user_id = create_admin_test_user('admin_test_put')
    form_data = {
        'id': user_id,
        'username': 'new',
        'password': 'new_pass',
    }
    request, response = waf.server.test_client.put('/admin/user/', json=form_data, headers=waf.default_headers)
    assert response.status == 200
    with get_engine('default').connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.id==user_id)
        row = con.execute(query)
        assert(row.fetchone().username == 'new')
