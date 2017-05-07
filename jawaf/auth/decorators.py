from sanic.request import Request
from sanic.response import json
from jawaf.auth.permissions import check_permission
from jawaf.auth.utils import login_redirect
from jawaf.exceptions import ServerError

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
        async def wrapped_view(*args, **kwargs):
            request = None
            if 'request' in kwargs:
                request = kwags['request']
            for arg in args:
                if type(arg) == Request:
                    request = arg
                    break
            if not request:
                raise ServerError('No request found!')
            if request['session'].get('user', None):
                return await view_func(*args, **kwargs)
            if self.redirect:
                return login_redirect(request)
            return json({'message': 'access denied'}, status=403)
        return wrapped_view

class has_permission(object):
    """Decorator to check if a logged in user has the specified permission.
    Works for class based or function views.
    Optionally takes an argument `redirect=True` to redirect to login automatically on failure.
    Default behavior is to return a json message `access denied` with a 403 status.
    """

    def __init__(self, name=None, target=None, redirect=False):
        """
        :param name: String: Permission name to check.
        :param target: String: Permission target to check.
        :param redirect: Boolean: Whether or not to redirect on failure.
        """
        self.name = name
        self.target = target
        self.redirect = redirect

    def __call__(self, view_func, *_args, **_kwargs):
        async def wrapped_view(*args, **kwargs):
            request = None
            if 'request' in kwargs:
                request = kwags['request']
            for arg in args:
                if type(arg) == Request:
                    request = arg
                    break
            if not request:
                raise ServerError('No request found!')
            user_row = request['session'].get('user', None)
            if user_row and await check_permission(user_row, self.name, self.target):
                return await view_func(*args, **kwargs)
            if self.redirect:
                return login_redirect(request)
            return json({'message': 'access denied'}, status=403)
        return wrapped_view

