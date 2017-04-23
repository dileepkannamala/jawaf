from sanic.response import redirect
from jawaf.conf import settings

def login_redirect(request):
    """Convenience method to return a redirect with "next" populated.
    :param request: Sanic request.
    :return: Redirect response.
    """
    return redirect('%s?next=%s' % (settings.AUTH_CONFIG['login_url'], request.path))