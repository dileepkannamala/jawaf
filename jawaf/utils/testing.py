import sanic.testing
from jawaf.conf import settings
# General util functions for testing.

def csrf_headers(request=None):
    csrf_token = request['session'].get('csrf_token', None) if request else None
    headers = {
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://%s:%s/' % (sanic.testing.HOST, sanic.testing.PORT),
    }
    if csrf_token:
        headers[settings.CSRF_HEADER_NAME] = csrf_token
    return headers

def simulate_login(waf, username, password, next='/'):
    """Simulate a login using the provided username and password.
    :param waf: Jawaf instance.
    :param username: String. Username.
    :param password: String. Password.
    :param next: String. Optional url path to redirect to.
    :return: Tuple. request, response.
    """
    login_form_data = {
        'username': username,
        'password': password,
        'next': next,
    }
    request, response = waf.server.test_client.post('/auth/login/', json=login_form_data, headers=csrf_headers())
    test_session_inject(waf, request['session'], ['user', 'csrf_token'])
    return request, response

def simulate_logout(waf, username):
    request, response = waf.server.test_client.post('/auth/logout/', json={'username': username}, headers=csrf_headers())
    test_session_inject(waf, {'user': None, 'csrf_token': None}, ['user', 'csrf_token'])

def test_session_inject(waf, session, keys):
    """The Sanic test client starts and stops the Sanic server for each request.
    Inject the specified keys from the session into the test client's middleware to persist it!
    This let's you log in with one request then access a protected view with another.
    :param waf: Jawaf Instance.
    :param session: sanic_session Session instance.
    :param keys: list. Keys from a previous session to inject into the new session.
    """
    @waf.server.test_client.app.middleware('request')
    async def add_session_to_request(request):
        for key in keys:
            if key in session:
                if session[key] is None:
                    request['session'].pop(key)
                else:
                    request['session'][key] = session[key]

