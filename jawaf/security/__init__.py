import re
RE_STRIP_HTTPS = re.compile('http[s]{0,1}\:\/\/')
RE_STRIP_PATH = re.compile('\/.*?')

#TODO: Evaluate using a token as well

# Reference:
# https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet#Protecting_REST_Services:_Use_of_Custom_Request_Headers

def check_headers(headers):
    """Test headers to protect against CSRF:

    :param headers: Dict.
    :return: Boolean. If check passes.
    """
    if not headers.get('x-requested-with', None) == 'XMLHttpRequest':
        return False
    origin = RE_STRIP_PATH.sub('', RE_STRIP_HTTPS.sub('', headers.get('origin', '')))
    host = headers.get('host', None)
    return origin == host
