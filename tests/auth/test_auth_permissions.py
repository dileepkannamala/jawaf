import pytest
import sqlalchemy as sa
from jawaf.auth import users, permissions
from jawaf.auth import tables
from jawaf.db import get_engine
from jawaf.utils import testing


@pytest.fixture(scope='module')
def create_groups():
    """Create test users."""
    engine = get_engine('default')
    users.create_user_sync(
        engine, username='permission_test_admin', password='admin_pass_1')
    users.create_user_sync(
        engine, username='permission_test_regular', password='admin_pass_2')
    group_id = permissions.create_group_sync(
        engine, name='AdminEditors',
        permission_pairs=({'name': 'get', 'target': 'test_app'},))
    with engine.connect() as con:
        query = sa.select('*').select_from(tables.user).where(
            tables.user.c.username == 'permission_test_admin')
        user_row = [r for r in con.execute(query)][0]
    permissions.add_user_to_group_sync(engine, user_row.id, group_id)


def test_read_only_permission_fail(test_project, waf, create_groups):
    """Test has permission works with readonly"""
    request, response = testing.simulate_login(
        waf, 'permission_test_regular', 'admin_pass_2')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get(
        '/test_app/read_only/', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 403


def test_read_only_permission_success(test_project, waf, create_groups):
    """Test has permission works with readonly"""
    request, response = testing.simulate_login(
        waf, 'permission_test_admin', 'admin_pass_1')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get(
        '/test_app/read_only/', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200
