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
