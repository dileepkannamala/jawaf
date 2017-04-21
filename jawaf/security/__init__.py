import hashlib
import hmac
import re
from jawaf.conf import settings

RE_STRIP_HTTPS = re.compile('http[s]{0,1}\:\/\/')
RE_STRIP_PATH = re.compile('\/.*?')

# Reference:
# https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet

def check_csrf_headers(headers):
    """Test headers to protect against CSRF and ensure:
        * x-requested-with is present and correct.
        * origin and host match.
    :param headers: Dict.
    :return: Boolean. If check passes.
    """
    if not headers.get('x-requested-with', None) == 'XMLHttpRequest':
        return False
    origin = RE_STRIP_PATH.sub('', RE_STRIP_HTTPS.sub('', headers.get('origin', '')))
    host = headers.get('host', None)
    return origin == host

def check_csrf(request):
    """Check for CSRF protection layers - headers & token.
    :param request: Sanic Request.
    :return: Boolean. If passes.
    """
    if not check_csrf_headers(request.headers):
        return False
    if not 'csrf_token' in request['session']:
        return False
    # First see if the token is in the headers:
    token = request.headers.get(settings.CSRF_HEADER_NAME, None)
    if not token:
        token = request.json.pop(settings.CSRF_FIELD_NAME, None)
        if not token:
            return False
    return token == request['session']['csrf_token']

def generate_csrf_token(user_id, user_last_login):
    """Generate csrf token from user id and user last login.
    :param user_id: Int. User id.
    :param user_last_login: Datetime. Last login datetime.
    :return: String. Token.
    """    
    message = bytearray('%s|%s' % (user_id, str(user_last_login)), 'utf-8')
    secret = bytearray(settings.SECRET_KEY, 'utf-8')
    return hmac.new(secret, msg=message, digestmod=hashlib.sha256).hexdigest()