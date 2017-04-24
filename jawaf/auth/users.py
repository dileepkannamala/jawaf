import base64
import datetime
import hashlib
import secrets
from argon2.exceptions import VerifyMismatchError
import sqlalchemy as sa
from jawaf.auth.tables import user, user_password_reset
from jawaf.auth.utils import database_key
from jawaf.conf import settings
from jawaf.db import Connection
from jawaf.security import generate_csrf_token
from jawaf.utils.timezone import get_utc

SELECTOR_ENCODED_LENGTH = 24
SELECTOR_TOKEN_LENGTH = 18

def check_password(password, encoded):
    """Verify the password using Password Hasher from settings.
    :param password: String. Plain text password to verify.
    :param encoded: String. Encoded password to check against.
    :return: Boolean. Whether or not password is verified.
    """
    try:
        return settings.PASSWORD_HASHER.verify(encoded, password)
    # TODO: This is specific to argon2 - find a more generic way to approach this?
    except VerifyMismatchError:
        return False

async def check_user(username='', password='', database=None):
    """Check a user username/password combination agains the database.
    :param username: String. Username to check.
    :param password: String. password to verify.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    :return: Boolean. If username and password are a valid combination.
    """
    database = database_key(database)
    async with Connection(database) as con:
        query = sa.select('*').select_from(user).where(user.c.username==username)
        row = await con.fetchrow(query)
        if not row:
            return False
        if check_password(password, row.password):
            return row
        return False

async def check_user_reset_access(username, user_id, split_token, database=None):
    """Check password reset token for the current user.
    :param username: String. Username to check.
    :param user_id: Int. User_id..
    :param split_token: String. Split token to search for and validate against.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    """
    if username is None or user_id is None:
        return False
    database = database_key(database)
    selector = split_token[:SELECTOR_ENCODED_LENGTH].encode('utf-8')
    verifier = split_token[SELECTOR_ENCODED_LENGTH:].encode('utf-8')
    async with Connection(database) as con:
        query = sa.select('*').select_from(user) \
            .where(user.c.username==username) \
            .where(user.c.id==user_id)
        row = await con.fetchrow(query)
        if not row:
            # username and id don't match!
            return False
        query = sa.select('*').select_from(user_password_reset) \
            .where(user_password_reset.c.selector==selector) \
            .where(user_password_reset.c.user_id==user_id)
        row = await con.fetchrow(query)
        if not row:
            # Selector not found - invalid link.
            return False
        if get_utc(datetime.datetime.now()) > row.expires:
            # First remove the expired record.
            stmt = user_password_reset.delete().where(user_password_reset.c.id==row.id)
            await con.execute(stmt)
            return False
        if hashlib.sha256(verifier).hexdigest() == row.verifier:
            # Only allow this reset token to be used once.
            stmt = user_password_reset.delete().where(user_password_reset.c.id==row.id)
            await con.execute(stmt)
            return True
        return False

async def create_user(username, 
    password, 
    first_name=None, 
    last_name=None,
    email=None,
    user_type=None,
    is_staff=False,
    is_superuser=False,
    is_active=True,
    date_joined=None,
    database=None):
    """Create a user.
    :param username: String. Username.
    :param password: String. Password. Will be stored encoded.
    :param first_name: String. User's first name. (Default None)
    :param last_name: String. User's last name. (Default None)
    :param user_type: String. Optionally segment users with string categories. (Default None)
    :param is_active: Boolean. If user account is active. (Default True)
    :param is_staff: Boolean. If user is "staff" and has "admin" level access. (Default False)
    :param is_superuser: Boolean. If user is a "superuser" and has all permissions without being explicitly assigned. (Default False)
    :param date_joined: Datetime (with timezone). Date user account was created.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    """
    database = database_key(database)
    if date_joined == None:
        date_joined = get_utc(datetime.datetime.now())
    async with Connection(database) as con:
        stmt = user.insert().values(
            username=username, 
            password=make_password(password), 
            first_name=first_name, 
            last_name=last_name,
            email=email,
            user_type=user_type,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            date_joined=date_joined,
            last_login=None)
        await con.execute(stmt)

def create_user_sync(engine, username='', 
    password='', 
    first_name=None, 
    last_name=None,
    email=None,
    user_type=None,
    is_staff=False,
    is_superuser=False,
    is_active=True,
    date_joined=None):
    """Create a user synchronously.
    :param engine: SQLAlchemy Engine. Engine to connect to. 
    :param username: String. Username.
    :param password: String. Password. Will be stored encoded.
    :param first_name: String. User's first name. (Default None)
    :param last_name: String. User's last name. (Default None)
    :param user_type: String. Optionally segment users with string categories. (Default None)
    :param is_active: Boolean. If user account is active. (Default True)
    :param is_staff: Boolean. If user is "staff" and has "admin" level access. (Default False)
    :param is_superuser: Boolean. If user is a "superuser" and has all permissions without being explicitly assigned. (Default False)
    :param date_joined: Datetime (with timezone). Date user account was created.
    """
    if not engine:
        raise Exception('Must specify an SQLAlchemy Engine')
    if date_joined == None:
        date_joined = get_utc(datetime.datetime.now())
    with engine.connect() as con:
        stmt = user.insert().values(
            username=username, 
            password=make_password(password), 
            first_name=first_name, 
            last_name=last_name,
            email=email,
            user_type=user_type,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            date_joined=date_joined,
            last_login=None)
        con.execute(stmt)

def decode_user_id(encoded_user_id):
    """Get decoded user_id.
    :param encoded_user_id: String. Encoded user_id..
    :return: Int. User id.
    """
    try:
        return int(base64.urlsafe_b64decode(encoded_user_id.encode('utf-8')))
    except:
        return None

def encode_user_id(user_id):
    """Encode the user id for use in URL.
    :param user_id: Int. User id to encode.
    :return: String. Encoded user id.
    """
    return base64.urlsafe_b64encode(bytes(str(user_id).encode('utf-8'))).decode('utf-8')

def _generate_split_token():
    selector = base64.urlsafe_b64encode(secrets.token_bytes(SELECTOR_TOKEN_LENGTH))
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(SELECTOR_TOKEN_LENGTH+6))
    return selector, verifier

async def generate_reset_split_token(user_id, database=None):
    """Generate a password reset token for the current user.
    :param user_id: Int. User id to generate split token for.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    :return: String. Joined token.
    """
    database = database_key(database)
    selector, verifier = _generate_split_token()
    async with Connection(database) as con:
        stmt = user_password_reset.insert().values(
            user_id=user_id,
            selector=selector,
            verifier=hashlib.sha256(verifier).hexdigest(),
            expires=get_utc(datetime.datetime.now()+datetime.timedelta(hours=settings.AUTH_CONFIG['password_reset_expiration'])),
            )
        await con.execute(stmt)
    return '%s%s' % (selector.decode('utf-8'), verifier.decode('utf-8'))

async def generate_password_reset_path(user_id, database=None):
    """Generate the reset url.
    :param user_id: Int. User id to generate split token for.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    :return: String. Path component of url to process reset.
    """
    encoded_user_id = encode_user_id(user_id)
    token = await generate_reset_split_token(user_id, database=database)
    return '/auth/password_reset/%s/%s/' % (encoded_user_id, token)

async def log_in(request, user_row):
    """Add the user to the session, update last_login.
    :param request: Sanic request.
    :param user_row: User SQLAlchmey result.
    """
    last_login = get_utc(datetime.datetime.now())
    request['session']['user'] = user_row
    request['session']['csrf_token'] = generate_csrf_token(user_row.id, user_row.last_login)
    await update_user(database=None, target_username=user_row.username, last_login=last_login)

async def log_out(request):
    """Remove the user from the session.
    :param request: Sanic request.
    """
    request['session'].pop('user')
    request['session']['csrf_token'] = generate_csrf_token()

def make_password(password):
    """Encode the password using Password Hasher from settings.
    :param password: String. Plain text password to hash.
    :return: String. Encoded (hashed) password.
    """
    return settings.PASSWORD_HASHER.hash(password)

async def update_user(database=None, target_username=None, target_user_id=None, **kwargs):
    """Update user. Accepts same optional kwargs as create_user + last_login.
    :param database: String. Database name to connect to. (Default: None - use jawaf.auth default)
    :param target_username: String. Username to search against.
    :param username: String. Username.
    :param password: String. Password. Will be stored encoded.
    :param first_name: String. User's first name. (Default None)
    :param last_name: String. User's last name. (Default None)
    :param user_type: String. Optionally segment users with string categories. (Default None)
    :param is_active: Boolean. If user account is active. (Default True)
    :param is_staff: Boolean. If user is "staff" and has "admin" level access. (Default False)
    :param is_superuser: Boolean. If user is a "superuser" and has all permissions without being explicitly assigned. (Default False)
    :param date_joined: Datetime (with timezone). Date user account was created.
    :param last_login: Datetime (with timezone). Date user account was last accessed.
    """
    database = database_key(database)
    if 'password' in kwargs:
        kwargs['password'] = make_password(kwargs['password'])
    if not target_username and not target_user_id:
        raise Exception('Must provide username or user_id to update')
    async with Connection(database) as con:
        if target_username:
            stmt = user.update().where(user.c.username==target_username).values(**kwargs)
        else:
            stmt = user.update().where(user.c.id==target_user_id).values(**kwargs)
        await con.execute(stmt)
