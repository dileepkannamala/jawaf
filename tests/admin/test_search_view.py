import pytest
import sqlalchemy as sa
from jawaf.auth import tables, users
from jawaf.conf import settings
from jawaf.db import get_engine
from jawaf.utils import testing

@pytest.fixture(scope='module')
def admin_login_user():
    engine = get_engine('default')
    username='admin_search_test'
    password='admin_search_pass'
    users.create_user_sync(engine, username=username, password=password, is_staff=True, is_superuser=True)
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username==username)
        results = con.execute(query)
        user_row = results.fetchone()
    return user_row.id, user_row.username, password

def test_search_get(test_project, waf, admin_login_user):
    """Test search for a user"""
    request, response = testing.simulate_login(waf, 'admin_search_test', 'admin_search_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get('/admin/user/search/?field=username&value=admin_search_test', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200

def test_search_get_bad_table(test_project, waf, admin_login_user):
    """Test search for a user"""
    request, response = testing.simulate_login(waf, 'admin_search_test', 'admin_search_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get('/admin/cats/search/?field=username&value=admin_search_test', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 403

def test_search_get_no_data(test_project, waf, admin_login_user):
    """Test search for a user"""
    request, response = testing.simulate_login(waf, 'admin_search_test', 'admin_search_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get('/admin/user/search/?field=username&value=waffles', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 401

def test_search_get_sort_limit_offset(test_project, waf, admin_login_user):
    """Test search for a user passing in a sort, limit, and offset"""
    request, response = testing.simulate_login(waf, 'admin_search_test', 'admin_search_pass')
    middleware = testing.injected_session_start(waf, request)
    paramstring = 'field=username&value=admin_search_test&sort=username&limit=10&offset=0'
    request, response = waf.server.test_client.get(f'/admin/user/search/?{paramstring}', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200

def test_search_get_sort_limit_offset_reverse(test_project, waf, admin_login_user):
    """Test search for a user passing in a sort, limit, and offset"""
    request, response = testing.simulate_login(waf, 'admin_search_test', 'admin_search_pass')
    middleware = testing.injected_session_start(waf, request)
    paramstring = 'field=username&value=admin_search_test&sort=-username&limit=10&offset=0'
    request, response = waf.server.test_client.get(f'/admin/user/search/?{paramstring}', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200