# Roadmap

## Intro

This "roadmap" is functioning more as a very informal unordered TODO list. Not everything on this list will be implemented, and some items not on this list might be implemented. The journey to 1.0 will invite decisions which could alter the behavior and structure of Jawaf.

So be forewarned this could get quite flexible.


## To Do List Items

### Auth
    * Groups
    * Permissions

### Admin site
    * User + Permission Checks for Admin Site
    * Search API
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

### DB
    * Support optionally using pooling?

### Email
    * Basic email support?

### Security
    * CSRF Token in addition to host/origin + custom header?

### Tests
    * More tests!
    * Evaluate using testing.postgresl

### PyPi Release
    * Put this up on PyPi

### Misc
    * Consider adding Jawaf instance to Request middleware

### Roadmap
    * Transfer this all into a real roadmap with version numbers and tourist traps.

## Unlikely (or Post 1.0)

### DB Support
    * [Mysql](https://github.com/aio-libs/aiomysql)

### Messaging
    * [Kafka](https://github.com/aio-libs/aiokafka)?