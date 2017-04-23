from sanic.request import Request
from sanic.response import json
from jawaf.auth.utils import login_redirect

class login_required(object):
    """Decorator to check if a user is logged in.
    Works for class based or function views.
    Optionally takes an argument `redirect=True` to redirect to login automatically on failure.
    Default behavior is to return a json message `access denied` with a 403 status.
    """

    def __init__(self, redirect=False):
        """
        :param redirect: Boolean: Whether or not to redirect on failure.
        """
        self.redirect = redirect

    def __call__(self, view_func, *_args, **_kwargs):
        def wrapped_view(*args, **kwargs):
            request = None
            if 'request' in kwargs:
                request = kwags['request']
            for arg in args:
                if type(arg) == Request:
                    request = arg
                    break
            if not request:
                raise Exception('No request found!')
            if request['session'].get('user', None):
                return view_func(*args, **kwargs)
            if self.redirect:
                return login_redirect(request)
            return json({'message': 'access denied'}, status=403)
        return wrapped_view
