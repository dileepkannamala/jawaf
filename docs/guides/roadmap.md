# Roadmap

## Intro

Not everything on this list will be implemented, and some items not on this list might be implemented. The journey to 1.0 will invite decisions which could alter the behavior and structure of Jawaf. So be forewarned this could get quite flexible.

This is divided into sections:

`Road to 1.0` is the more or less official list of upcoming releases (including the first release to PyPi).

`Unversioned ToDo List` is a list of things that may or may not make it into the semi-official roadmap.

`Unlikely` is a list of itmes that have been evaluated and won't likely make it into the core for 1.0 (unless there's a real desire for those features).

## Road to 1.0

### 0.1.0

#### Auth
    * Groups
    * Permissions

#### Admin site
    * User + Permission Checks for Admin Site
    * Search API
    * Audit Trail of Actions

#### Email
    * Basic email support

#### PyPi Release
    * Put this up on PyPi

### 0.2.0

#### Migration
    * SQLAlchemy migration tool (alembic?)

#### Forms & Validation
    * Django Style Forms?
    * Validation (separated from Forms)

## Unversioned ToDo List

### Deploy/Run Options
    * [Gunicorn Support](https://pypi.python.org/pypi/sanic-gunicorn)
    * Docker Support?
    * ASGI Support?

#### DB
    * Support optionally using pooling?

#### Tests
    * More tests
    * testing.postgresl instead of actual postgres as an option

#### Misc
    * Consider adding Jawaf instance to Request middleware

## Unlikely

#### DB Support
    * [Mysql](https://github.com/aio-libs/aiomysql)

#### Messaging
    * [Kafka](https://github.com/aio-libs/aiokafka)?
