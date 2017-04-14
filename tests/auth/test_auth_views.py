import pytest
import sqlalchemy as sa
from jawaf.auth import users
from jawaf.auth.tables import user
from jawaf.db import get_engine

def _test_session_inject(test_client, session, keys):
    """The Sanic test client starts and stops the Sanic server for each request.
    Inject the specified keys from the session into the test client's middleware to persist it!
    This let's you log in with one request then access a protected view with another.
    :param test_client: Sanic Test Client instance.
    :param session: sanic_session Session instance.
    :param keys: list. Keys from a previous session to inject into the new session.
    """
    @test_client.app.middleware('request')
    async def add_session_to_request(request):
        for key in keys:
            request['session'][key] = session[key]

@pytest.fixture(scope='module')
def create_users():
    """Create test users."""
    engine = get_engine('default')
    users.create_user_from_engine(engine, username='admin', password='admin_pass')
    users.create_user_from_engine(engine, username='casual_user', password='casual_pass')

def test_login_post(test_project, waf, create_users):
    """Test logging in via post."""
    form_data = {
        'username': 'admin',
        'password': 'admin_pass',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', data=form_data)
    assert 'user' in request['session']
    assert request['session']['user'].username == 'admin'
    assert response.status == 200

def test_login_post_no_password(test_project, waf, create_users):
    """Test logging in via post without a password."""
    form_data = {
        'username': 'admin',
        'password': '',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', data=form_data)
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_post_wrong_password(test_project, waf, create_users):
    """Test logging in via post with the wrong password."""
    form_data = {
        'username': 'admin',
        'password': 'puppies',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', data=form_data)
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_post_wrong_user(test_project, waf, create_users):
    """Test logging in via post with a nonexistent user."""
    form_data = {
        'username': 'gozer',
        'password': 'admin_pass',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', data=form_data)
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_required(test_project, waf, create_users):
    """Test accessing a view behind the login_required decorator while logged in."""
    form_data = {
        'username': 'admin',
        'password': 'admin_pass',
        'next': '/',
    }
    test_client = waf.server.test_client
    request, response = test_client.post('/auth/login/', data=form_data)
    _test_session_inject(test_client, request['session'], ['user'])
    request, response = test_client.get('/test_app/protected/')
    assert 'Protected!' in response.text
    assert response.status == 200

def test_login_required_not_logged_in(test_project, waf, create_users):
    """Test accessing a view behind the login_required decorator while not logged in."""
    test_client = waf.server.test_client
    _test_session_inject(test_client, {'user': None}, ['user']) # Ensure user isn't logged in via testing artifact.
    request, response = test_client.get('/test_app/protected/')
    assert 'Protected!' not in response.text
    assert 'login' in response.text
    assert response.status == 200

def test_logout_post(test_project, waf, create_users):
    """Test logging out via post."""
    form_data = {
        'username': 'admin',
        'password': 'admin_pass',
        'next': '/',
    }
    test_client = waf.server.test_client
    request, response = test_client.post('/auth/login/', data=form_data)
    _test_session_inject(test_client, request['session'], ['user'])
    request, response = test_client.post('/auth/logout/')
    assert not 'user' in request['session']
    assert response.status == 200

def test_password_change(test_project, waf, create_users):
    """Test changing password via post."""
    login_form_data = {
        'username': 'casual_user',
        'password': 'casual_pass',
        'next': '/',
    }
    change_form_data = {
        'username': 'casual_user',
        'old_password': 'casual_pass',
        'new_password': 'casual_pass2',
    }
    test_client = waf.server.test_client
    request, response = test_client.post('/auth/login/', data=login_form_data)
    _test_session_inject(test_client, request['session'], ['user'])
    request, response = test_client.post('/auth/password_change/', data=change_form_data)
    assert response.status == 200

def test_password_change_wrong_user(test_project, waf, create_users):
    """Test changing password for another user via post."""
    login_form_data = {
        'username': 'casual_user',
        'password': 'casual_pass',
        'next': '/',
    }
    change_form_data = {
        'username': 'admin',
        'old_password': 'admin_pass',
        'new_password': 'casual_pass2',
    }
    test_client = waf.server.test_client
    request, response = test_client.post('/auth/login/', data=login_form_data)
    _test_session_inject(test_client, request['session'], ['user'])
    request, response = test_client.post('/auth/password_change/', data=change_form_data)
    assert response.status == 403
