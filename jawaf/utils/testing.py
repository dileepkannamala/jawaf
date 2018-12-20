import sanic.testing
from jawaf.conf import settings


class MockSMTP(object):
    def __init__(self, *args, **kwargs):
        pass

    async def connect(self):
        pass

    async def sendmail(self, *args, **kwargs):
        pass


def csrf_headers(request=None):
    """Get the CSRF protection headers to pass into a test HTTP request.
    :param request: Sanic Request instance.
    :return: Dict. Headers.
    """
    headers = {
        'x-requested-with': 'XMLHttpRequest',
        'origin': f'https://{sanic.testing.HOST}:{sanic.testing.PORT}/',
    }
    csrf_token = request['session'].get('csrf_token', None) if request \
        else 'test_token'
    if csrf_token:
        headers[settings.CSRF_HEADER_NAME] = csrf_token
    return headers


def simulate_login(waf, username, password, next_path='/'):
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
        'next': next_path,
    }
    request, response = waf.server.test_client.post(
        '/auth/login/', json=login_form_data, headers=csrf_headers())
    return request, response


def simulate_request(waf):
    """Simulate a generic request to get the unauthenticated csrf token.
    :param waf: Jawaf instance.
    :return: Tuple. request, response.
    """
    request, response = waf.server.test_client.get('/', headers=csrf_headers())
    return request, response


def injected_session_end(waf, injected_session_middleware):
    """Remove the middleware so they don't keep piling up.
    :param waf: Jawaf instance.
    :param injected_session_middleware: Middelware method to remove.
    """
    waf.server.request_middleware.remove(injected_session_middleware)


def injected_session_start(waf, request):
    """Initialize an injected session via Sanic middleware
    :param waf: Jawaf instance.
    :param request: Sanic request from a previous interaction.
    :return: Sanic middleware method.
    """
    return test_session_inject(waf, request['session'], ['user', 'csrf_token'])


def test_session_inject(waf, session, keys):
    """The Sanic test client starts and stops the Sanic server for each request.
    Inject the specified keys from the session into the test client's
    next request via middleware!
    This let's you log in with one request then access a protected view
    with another.
    Just be sure to call injected_session_end afterwards to clean up.
    :param waf: Jawaf Instance.
    :param session: sanic_session Session instance.
    :param keys: list. Keys from a previous session to inject into
    the new session.
    :return: Sanic middleware method.
    """
    @waf.server.test_client.app.middleware('request')
    async def add_session_to_request(request):
        for key in keys:
            if key in session:
                if session[key] is None:
                    if key in request['session']:
                        request['session'].pop(key)
                else:
                    request['session'][key] = session[key]
    return add_session_to_request
