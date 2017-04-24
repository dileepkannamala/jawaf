import datetime
import hashlib
import pytest
import sqlalchemy as sa
from jawaf.auth import users
from jawaf.auth.tables import user, user_password_reset
from jawaf.db import get_engine
from jawaf.utils.timezone import get_utc
from jawaf.utils import testing

@pytest.fixture(scope='module')
def create_users():
    """Create test users."""
    engine = get_engine('default')
    users.create_user_sync(engine, username='admin', password='admin_pass')
    users.create_user_sync(engine, username='casual_user', password='casual_pass')

def test_login_post(test_project, waf, create_users):
    """Test logging in via post."""
    form_data = {
        'username': 'admin',
        'password': 'admin_pass',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', json=form_data, headers=testing.csrf_headers())
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
    request, response = waf.server.test_client.post('/auth/login/', json=form_data, headers=testing.csrf_headers())
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_post_wrong_password(test_project, waf, create_users):
    """Test logging in via post with the wrong password."""
    form_data = {
        'username': 'admin',
        'password': 'puppies',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', json=form_data, headers=testing.csrf_headers())
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_post_wrong_user(test_project, waf, create_users):
    """Test logging in via post with a nonexistent user."""
    form_data = {
        'username': 'gozer',
        'password': 'admin_pass',
        'next': '/',
    }
    request, response = waf.server.test_client.post('/auth/login/', json=form_data, headers=testing.csrf_headers())
    assert 'user' not in request['session']
    assert response.status == 403

def test_login_required(test_project, waf, create_users):
    """Test accessing a view behind the login_required decorator while logged in."""
    request, response = testing.simulate_login(waf, 'admin', 'admin_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.get('/test_app/protected/')
    testing.injected_session_end(waf, middleware)
    assert 'Protected!' in response.text
    assert response.status == 200

def test_login_required_not_logged_in(test_project, waf, create_users):
    """Test accessing a view behind the login_required decorator while not logged in."""
    request, response = waf.server.test_client.get('/test_app/protected_403/')
    assert response.status == 403

def test_login_required_not_logged_in_redirect(test_project, waf, create_users):
    """Test accessing a view behind the login_required decorator while not logged in."""
    request, response = waf.server.test_client.get('/test_app/protected/')
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
    request, response = testing.simulate_login(waf, 'admin', 'admin_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/auth/logout/', headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert not 'user' in request['session']
    assert response.status == 200

def test_password_change(test_project, waf, create_users):
    """Test changing password via post."""
    change_form_data = {
        'username': 'casual_user',
        'old_password': 'casual_pass',
        'new_password': 'casual_pass2',
    }
    request, response = testing.simulate_login(waf, 'casual_user', 'casual_pass')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/auth/password_change/', json=change_form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 200

def test_password_change_wrong_user(test_project, waf, create_users):
    """Test changing password for another user via post."""
    change_form_data = {
        'username': 'admin',
        'old_password': 'admin_pass',
        'new_password': 'casual_pass2',
    }
    request, response = testing.simulate_login(waf, 'casual_user', 'casual_pass2')
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/auth/password_change/', json=change_form_data, headers=testing.csrf_headers(request))
    testing.injected_session_end(waf, middleware)
    assert response.status == 403

def test_password_reset(test_project, waf, create_users):
    """Test changing password via post."""
    change_form_data = {
        'username': 'test',
        'new_password': 'wookies',
    }
    selector, verifier = users._generate_split_token()
    token = '%s%s' % (selector.decode('utf-8'), verifier.decode('utf-8'))
    with get_engine().connect() as con:
        query = sa.select('*').select_from(user)
        row = con.execute(query).fetchone()
        change_form_data['username'] = row.username
        stmt = user_password_reset.insert().values(
            user_id=row.id,
            selector=str(selector),
            verifier=hashlib.sha256(verifier).hexdigest(),
            expires=get_utc(datetime.datetime.now()+datetime.timedelta(hours=3)),
            )
        con.execute(stmt)
    encoded_user_id = users.encode_user_id(row.id)
    request, response = testing.simulate_request(waf)
    middleware = testing.injected_session_start(waf, request)
    request, response = waf.server.test_client.post('/auth/password_reset/%s/%s/' % (encoded_user_id, token), json=change_form_data, headers=testing.csrf_headers())
    testing.injected_session_end(waf, middleware)
    assert response.status == 200
