import datetime
from argon2.exceptions import VerifyMismatchError
import sqlalchemy as sa
from jawaf.auth.tables import user
from jawaf.conf import settings
from jawaf.db import Connection
from jawaf.utils.timezone import get_utc

def _database_key(database):
    """Get the default database key for jawaf.auth
    :param database: String. Database name to connect to.
    """
    if not database:
        return settings.AUTH_CONFIG['database']
    return database

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
    database = _database_key(database)
    async with Connection(database) as con:
        query = sa.select('*').select_from(user).where(user.c.username==username)
        row = await con.fetchrow(query)
        if not row:
            return False
        if check_password(password, row.password):
            return row
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
    database = _database_key(database)
    encoded = make_password(password)
    if date_joined == None:
        date_joined = get_utc(datetime.datetime.now())
    async with Connection(database) as con:
        stmt = user.insert().values(
            username=username, 
            password=encoded, 
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

def create_user_from_engine(engine, username='', 
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
    encoded = make_password(password)
    if date_joined == None:
        date_joined = get_utc(datetime.datetime.now())
    with engine.connect() as con:
        stmt = user.insert().values(
            username=username, 
            password=encoded, 
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

async def log_in(request, user_row):
    request['session']['user'] = user_row
    update_user(database=None, target_username=user_row.username, last_login=get_utc(datetime.datetime.now()))

async def log_out(request, user_row):
    request['session'].pop('user')

def make_password(password):
    """Encode the password using Password Hasher from settings.
    :param password: String. Plain text password to hash.
    :return: String. Encoded (hashed) password.
    """
    return settings.PASSWORD_HASHER.hash(password)

async def update_user(database=None, target_username='', **kwargs):
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
    database = _database_key(database)
    if 'password' in kwargs:
        kwargs['password'] = make_password(kwargs['password'])
    async with Connection(database) as con:
        stmt = user.update().where(user.c.username==target_username).values(**kwargs)
        await con.execute(stmt)
