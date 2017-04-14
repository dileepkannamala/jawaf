# Roadmap

## Intro

This "roadmap" is functioning more as a very informal unordered TODO list. Not everything on this list will be implemented, and some items not on this list might be implemented. The journey to 1.0 will invite decisions which could alter the behavior and structure of Jawaf.

So be forewarned this could get quite flexible.


## To Do List Items

### ORM
    * Take a fresh look and evaluate if it makes sense to attempt SQLAlchemy ORM support.
    * (Possible Lightweight ORM like layer?)
    * Evaluate building a general internal API for CRUD and rows

### Auth
    * reset password
    * Groups
    * Permissions

### DB Support
    * [Mysql](https://github.com/aio-libs/aiomysql)
    * Some other db...

### Tests
    * More tests!
    * Evaluate using testing.postgresl and testing.mysqld
    * Performance considerations
    * Practical use cases
    * Benchmarks?

### Forms & Validation
    * Django Style Forms?
    * Validation (separated from Forms)

### Migration
    * SQLAlchemy migration tool (alembic?)

### Deploy/Run Options
    * Docker Support?
    * ASGI Support?
    * Gunicorn Support (via Sanic)

### Admin site
    * Register Tables
    * Basic CRUD API
    * Audit Trail of Actions

### Self Documenting Endpoints
    * Look into this?

### Messaging
    * [Kafka](https://github.com/aio-libs/aiokafka)?

### PyPi Release
    * Put this up on PyPi

### Roadmap
    * Transfer this all into a real roadmap with version numbers and tourist traps.
