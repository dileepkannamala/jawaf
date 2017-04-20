# Admin API

## Introduction

Jawaf provides a basic, optional RESTful interface to build an admin site on.

## Setup

By default jawaf.admin is in INSTALLED_APPS in `settings.py`, and you'll find entries in your project `routes.py` as well.

## Registering Tables

To use the admin views you will need to register the tables you wish to access through the admin.

Editing `polls/tables.py`

```python
from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, Table, Text
from jawaf.admin import registry

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

### Adding in admin registry!
registry.register('question', question, DATABASE)
registry.register('choice', choice, DATABASE)
```

The `name` is the first argument to register, and tells the admin what `name` to use as a lookup reference when processing urls.

## CRUD

You can hit `/admin/question/` to access CRUD operations on the `question` table. Supported operations:

**delete** - pass in a json body with `id` specified to delete the matching `question` row.

**get** - Add `id` to the url params to get a json object containing a success message and the data from the matching `question` row.

**post** - pass in a json body with the columns and values in a dictionary to create a new `question` row.

**put** - pass in a json body with `id` specified plus the columns and values - all in a single dictionary to edit an existing `question` row.


## Current Status
 
Very much in progress. Basic features are still being completed and will need reviewing. See the roadmap for reference.