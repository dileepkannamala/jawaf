# Advanced Notes

## Management Commands

jawaf supports the following management commands:

    * `create-tables`
    * `help`
    * `run`
    * `shell`
    * `start-app`
    * `start-project`
    * `test`

You can also add your own in a manner similar to Django:

Editing `polls/management/commands/say_hi.py`
(Note: You do not need `__init__.py` files with Python 3)

```python
from jawaf.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', help='A name')

    def handle(self, **options):
        print('Hi!')
        print(options)
```

Unlike Django, jawaf leaves positional arguments inside of `**options`
rather than breaking them out into `*args`.

## Testing Database Interactions

If you want to test Database interactions asynchronously outside of the built in test client Sanic provides,
you need to initialize and destroy the database pools manually before using the jawaf.db.Connection class.

Here's a rough example:

Viewing `tests/test_poll_tables.py`:

```python
from jawaf.db import Connection
import pytest
import sqlalchemy as sa

pytest.mark.ascynio
async def test_polls_question_created(waf):
    await waf.create_database_pool('default')
    async with Connection() as con:
        assert # sqlalchemy tests go here
    await waf.close_database_pools()
```

## Database Migrations

Jawaf supports migrations through the use of [Alembic](http://alembic.zzzcomputing.com/en/latest/).
On project start a default Alembic environment is automatically created under the `migrations` directory. (This is also where `alembic.ini` lives). `env.py` is customized to automatically pull in SQLAlchemy metadata for all apps listed in `INSTALLED_APPS` in settings. It will also override the connection string using the default database in `settings.py`. (If you want to support multiple databases you will need to follow the [Instructions in the Alembic Docs](http://alembic.zzzcomputing.com/en/latest/branches.html#working-with-multiple-bases) to do so.

Alembic commands are passed directly to alembic via the management command `db`. Example:

```
python manage.py db revision -m "Add a column"
```

`python manage.py db` becomes a drop in replacement for `alembic --config=migrations/alembic.ini`.

## Installed Apps and Modules

In addition to apps defined within your Jawaf project, you can reference any
installed python module that follows the basic structure of a Jawa app.
The Jawaf auth module is an example.
Let's consider another: The `bananas` project.

We set up the directory structure as follows:

```python
bananas/
    management/
        commands/
            peel_bananas.py
    routes.py
    tables.py
    views.py
```

The sub-directory is important, as the `.` character will let Jawaf know how to import this app.

Including it is as simple as adding it to INSTALLED_APPS:

Editing `mysite/settings.py`

```python
INSTALLED_PACKAGES = [
    'jawaf.auth',
    'bananas',
    'polls',
]
```

Editing `mysite/routes.py`

```python
routes = [
    {'uri': '/auth/', 'include': 'jawaf.auth'},
    {'uri': '/bananas/', 'include': 'bananas.app'},
    {'uri': '/polls/', 'include': 'polls'},
]
```

You can also run custom initialization code when Jawaf loads:

Editing `bananas/__init__.py`

```python

# Code that defines a Banana class

def initialize(waf):
    waf.banana = Banana()
```

## Connecting to Multiple Databases

Viewing `settings.py`:

```python
DATABASES = {
    'default': {
        'database': 'jawaf_mysite', # Default database name - change to match the database you want to use.
        'engine': 'postgresql',
        'host': 'localhost', # Set this to the host for your postgresql install, localhost by default.
        'password': 'abcd', # Set this to the password for your postgresql install
        'user': 'a_user', # Set this to the user for your postgresql install
    },
    'external': {
        'database': 'external_data', # Default database name - change to match the database you want to use.
        'engine': 'postgresql',
        'host': 'localhost', # Set this to the host for your postgresql install, localhost by default.
        'password': 'efg', # Set this to the password for your postgresql install
        'user': 'b_user', # Set this to the user for your postgresql install
    },
}
```

Let's say you wanted to pull `name` from the table `user` in the `default` database,
and `email` from the table `old_customer` in the `external` database.

```python
from jawaf.db import Connection

async def show(request):
    # return text('Meow!')
    async with Connection('default') as con:
        # SQLAlchemy/db calls here will reference the 'default' database
    async with Connection('external') as con:
        # SQLAlchemy/db calls here will reference the 'external' database
    return # combined data
```

## CSRF Protection

Jawaf provides CSRF Protection using the [OWasp CSRF Cheat Sheet](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet) as a reference.

For the auth and admin apps, interaction is via RESTful services which expect:

### Headers

The `X-Requested-With: XMLHttpRequest` header must be present with the correct value. The `host` and `origin` headers must match as well.

### CSRF Token

A random csrf token is used for each session. This token is altered on login, and again on logout.
It can either be present in a json field (`settings.CSRF_FIELD_NAME` controls the name, `csrf_token` by default), or in a header (`settings.CSRF_HEADER_NAME`, `X-CSRF-TOKEN` by default).

It can be accessed via the session:

```python
request['session']['csrf_token']
```

## Sending Email

After configuing settings to point to an SMTP server:

```python
SMTP = {
    'host':'localhost',
    'port': 8025,
    'username': '', # Optional, default blank
    'password': '', # Optional, default blank
    'ssl': False, # Optional, default False
}
```

You can use the async function `send_mail`.
The recipient address arguments (`to`, `cc`, and `bcc`) all accept either a string or a list of strings.

`html_message` will create a multipart email with `message` as a text alternative to the `html_message`.

```python
from jawaf.mail import send_mail

async def send_email(request):
    await send_mail(subject=request.json.get('subject'),
        message=request.json.get('message'), 
        from_address=request.json.get('from_address'), 
        to=request.json.get('to'), 
        cc=request.json.get('cc', None),
        bcc=request.json.get('bcc', None),
        html_message=request.json.get('html_message', None)
    )
```

## Jawaf Exceptions

Jawaf defines the following exceptions (in `jawaf.exceptions`):

* ConfigurationError - Problem with configuration (settings.py)

* ManagementError - Problem with management commands

* ServerError - General Purpose Jawaf Error

* ValidationError - Validation failed


## Validators

Jawaf Validators provide a base class for custom validation of data.

Editing `polls/validators.py`

```python
from jawaf.validators import Validator
from mysite.polls.tables import choice

class ChoiceValidator(Validator):
    __table__ = choice
    def validate_votes(self, value):
        if not isinstance(value, int): return False
        return (value > -1)
```

Usage:

```python
def edit_choice(request):
    validator = ChoiceValidator(data=request.json)
    if not validator.is_valid():
        do_something_with(validator.invalidated_data)
    else:
        do_something_with(validator.validated_data)
```

You can also define the class without specifying `__table__`. This is useful if you want to validate data that spans multiple tables, or that isn't directly tied to a table.
