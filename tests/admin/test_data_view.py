import pytest
import sqlalchemy as sa
from jawaf.auth import tables, users
from jawaf.conf import settings
from jawaf.db import get_engine
from jawaf.utils import testing

def create_admin_test_data_user(name, password='admin_pass_test'):
    """Create test users."""
    engine = get_engine('default')
    users.create_user_sync(engine, username=name, password=password)
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username==name)
        results = con.execute(query)
        user_row = results.fetchone()
    return user_row.id, user_row.username, password

@pytest.fixture(scope='module')
def admin_login_user():
    engine = get_engine('default')
    username='admin_api_test'
    password='admin_api_pass'
    users.create_user_sync(engine, username=username, password=password, is_staff=True, is_superuser=True)
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username==username)
        results = con.execute(query)
        user_row = results.fetchone()
    return user_row.id, user_row.username, password

def test_data_delete(test_project, waf, admin_login_user):
    """Test posting a new user"""
    user_id, username, password = create_admin_test_data_user('admin_test_delete')
    form_data = {
        'id': user_id,
    }
    request, response = testing.simulate_login(waf, 'admin_api_test', 'admin_api_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.delete('/admin/user/', json=form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200

def test_data_get(test_project, waf, admin_login_user):
    """Test posting a new user"""
    user_id, username, password = create_admin_test_data_user('admin_test_get')
    request, response = testing.simulate_login(waf, 'admin_api_test', 'admin_api_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get(f'/admin/user/?id={user_id}', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200

def test_data_post(test_project, waf, admin_login_user):
    """Test posting a new user"""
    form_data = {
        'username': 'cool',
        'password': 'cool_pass',
        'is_active': True,
        'is_staff': True,
    }
    request, response = testing.simulate_login(waf, 'admin_api_test', 'admin_api_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/admin/user/', json=form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 201

def test_data_post_not_logged_in(test_project, waf, admin_login_user):
    """Test posting a new user when not logged in"""
    form_data = {
        'username': 'cool',
        'password': 'cool_pass',
        'is_active': True,
        'is_staff': True,
    }
    request, response = testing.simulate_request(waf)
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/admin/user/', json=form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 403

def test_data_post_no_csrf(test_project, waf, admin_login_user):
    """Test posting a new user"""
    form_data = {
        'username': 'cool',
        'password': 'cool_pass',
        'is_active': True,
        'is_staff': True,
    }
    request, response = testing.simulate_login(waf, 'admin_api_test', 'admin_api_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/admin/user/', json=form_data, headers=testing.csrf_headers())
    testing.injected_session_end(waf, middleware)
    assert response.status == 403

def test_data_patch(test_project, waf, admin_login_user):
    """Test posting a new user"""
    user_id, username, password = create_admin_test_data_user('admin_test_put')
    form_data = {
        'id': user_id,
        'username': 'new',
        'password': 'new_pass',
    }
    request, response = testing.simulate_login(waf, 'admin_api_test', 'admin_api_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.patch('/admin/user/', json=form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200
    with get_engine('default').connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.id==user_id)
        row = con.execute(query)
        assert(row.fetchone().username == 'new')
