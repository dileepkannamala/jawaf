import pytest
import sqlalchemy as sa
from jawaf.auth import tables, users
from jawaf.conf import settings
from jawaf.db import get_engine
from jawaf.utils import testing

@pytest.fixture(scope='module')
def admin_login_user():
    engine = get_engine('default')
    username='admin_manage_access_test'
    password='admin_manage_access_pass'
    users.create_user_sync(engine, username=username, password=password, is_staff=True, is_superuser=True)
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(tables.user.c.username==username)
        results = con.execute(query)
        user_row = results.fetchone()
    return user_row.id, user_row.username, password

def test_manage_access_post(test_project, waf, admin_login_user):
    """Test posting a new group and adding a user"""
    data = {
        'user_ids': [admin_login_user[0]],
        'group_name': 'test_access',
        'permissions': [
            {'name': 'get', 'target': 'admin'},
            {'name': 'post', 'target': 'admin'},
        ],
    }
    request, response = testing.simulate_login(waf, 'admin_manage_access_test', 'admin_manage_access_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/admin/manage_access/', json=data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200
