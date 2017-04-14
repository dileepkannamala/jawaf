# Getting Started

## Starting a Project

Jawaf uses projects in a similar manner to Django. It is a collection of apps and settings representing a particular website or web application.

`jawaf-admin start-project mysite`

This command creates scaffolding for an jawaf application:

```python
mysite/
    manage.py
    mysite/
        settings.py
        routes.py
```

**Creating Your First App**

`python manage.py start-app polls`

This will create a directory `polls` within the `mysite` root directory.

```python
mysite/
    mysite/
    polls/
        tables.py
        routes.py
        tests.py
        views.py
```

## Writing Your First View

Editing `polls/views.py`

```python
from sanic.response import text
from sanic.views import HTTPMethodView

async def hello(request):
    return text('Hello World!!!')

class GreetingsView(HTTPMethodView):
    async def get(self, request):
        return text('Greetings, World! It is a pleasure!')
```

Editing `polls/routes.py`

```python
from mysite.polls.views import hello, GreetingsView

routes = [
    {'uri': '', 'handler': hello},
    {'uri': 'formal/', 'handler': GreetingsView.as_view()},
]
```

Editing `mysite/settings.py`

```python
INSTALLED_APPS = [
    'jawaf.auth',
    'polls', # Add in the path to the local polls app
]
```

Editing `mysite/routes.py`

```python
routes = [
    {'uri': '/polls/', 'include': 'polls'},
]
```

## Running the Server

```
python manage.py run
```

Open [http://0.0.0.0:8080](http://0.0.0.0:8080/polls/) in your browser, or navigate to [http://0.0.0.0:8080/formal](http://0.0.0.0:8080/polls/formal/) for a more refined experience.

## Database Setup

Setting up the database (and any admin users) is up to you.
Right now - Jawaf only supports Postgresql. This *might* change in the future to also support Mariadb.

## Tables

Instead of Django's models (and an ORM), Jawaf uses SQLAlchemy's Core (vs it's ORM).

Editing `polls/tables.py`

```python
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, Table, Text

metadata = MetaData()

question = Table('polls_question', metadata,
    Column('id', Integer, primary_key=True),
    Column('question_text', Text()),
    Column('pub_date', DateTime(timezone=True)),
    )

choice = Table('polls_choice', metadata,
    Column('id', Integer, primary_key=True),
    Column('question_id', Integer, ForeignKey('polls_question.id'), nullable=False),
    Column('choice_text', Text()),
    Column('votes', Integer()),
    )

# Optionally you can specify the database the tables in this file should use.
DATABASE = 'default'
```

Editing `mysite/settings.py`

```python
INSTALLED_APPS = [
    'polls',
]
```

```
python manage.py create-tables polls
```

### Adding Data

```
python manage.py shell
```

At the shell:

```python
import datetime
from jawaf.db import get_engine
import sqlalchemy as sa
from mysite.polls.tables import question
engine = get_engine('default')
con = engine.connect()
stmt = question.insert().values(question_text='How?!', pub_date=datetime.datetime.now())
con.execute(stmt)
```

### Updating Views

```python
from sanic.response import text
from sanic.views import HTTPMethodView
### Adding imports for the database connection, sqlalchemy, and one of our new tables.
from jawaf.db import Connection
import sqlalchemy as sa
from mysite.polls.tables import question

async def hello(request):
    return text('Hello World!!!')

class GreetingsView(HTTPMethodView):
    async def get(self, request):
        return text('Greetings, World! It is a pleasure!')

### New Code! ###
async def query(request):
    query = sa.select('*').select_from(question)
    results = ''
    async with Connection() as con:
        row = await con.fetchrow(query)
        results += '%s\n' % str(row)
    return text(results)
```

## Writing Some Tests

Editing `polls/tests/test_polls_views.py`

```python
def test_query(waf):
    request, response = waf.server.test_client.get('/polls/query/')
    newlines = response.text.count('\n')
    assert newlines > 0
```

## Running Tests

```
python manage.py test
python manage.py test --args='-x --cov=./'
```
