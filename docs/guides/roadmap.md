# Roadmap

## Intro

This "roadmap" is functioning more as a very informal unordered TODO list. Not everything on this list will be implemented, and some items not on this list might be implemented. The journey to 1.0 will invite decisions which could alter the behavior and structure of Jawaf.

So be forewarned this could get quite flexible.


## To Do List Items

### Auth
    * Groups
    * Permissions

### ORM
    * General internal API for CRUD and rows - ORM Like Layer

### Admin site
    * Register Tables
    * Basic CRUD API
    * Audit Trail of Actions

### Forms & Validation
    * Django Style Forms?
    * Validation (separated from Forms)

### Migration
    * SQLAlchemy migration tool (alembic?)

### Deploy/Run Options
    * [Gunicorn Support](https://pypi.python.org/pypi/sanic-gunicorn)
    * Docker Support?
    * ASGI Support?

### Tests
    * More tests!
    * Evaluate using testing.postgresl and testing.mysqld
    * Performance considerations
    * Practical use cases
    * Benchmarks?

### DB Support
    * [Mysql](https://github.com/aio-libs/aiomysql)
    * Some other db...

### Messaging
    * [Kafka](https://github.com/aio-libs/aiokafka)?

### PyPi Release
    * Put this up on PyPi

### Roadmap
    * Transfer this all into a real roadmap with version numbers and tourist traps.
