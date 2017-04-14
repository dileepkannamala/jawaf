from functools import wraps
from sanic.response import redirect
from jawaf.conf import settings
# Taken from Django and edited to suit Jawaf's purposes.

def user_passes_test(test_func):
    """Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.

    :param test_func: Test function to apply
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_row = request['session'].get('user', None)
            if (user_row and test_func and test_func(user_row)) or \
            (user_row and test_func == None):
                return view_func(request, *args, **kwargs)
            return redirect('%s?next=%s' % (settings.AUTH_CONFIG['login_url'], request.path))
        return _wrapped_view
    return decorator

def login_required(view_func=None):
    """Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    decorator = user_passes_test(None)
    if view_func:
        return decorator(view_func)
    return decorator
