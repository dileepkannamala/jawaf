from sanic.response import redirect
from jawaf.conf import settings

def database_key(database):
    """Get the default database key for jawaf.auth
    :param database: String. Database name to connect to.
    """
    if not database:
        return settings.AUTH_CONFIG['database']
    return database

def login_redirect(request):
    """Convenience method to return a redirect with "next" populated.
    :param request: Sanic request.
    :return: Redirect response.
    """
    return redirect('{0}?next={1}'.format(settings.AUTH_CONFIG['login_url'], request.path))