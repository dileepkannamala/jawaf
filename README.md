
## Jawaf

[![Build Status](https://travis-ci.org/danpozmanter/jawaf.svg?branch=master)](https://travis-ci.org/danpozmanter/jawaf)
[![Documentation](https://readthedocs.org/projects/jawaf/badge/?version=latest)](http://jawaf.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/jawaf.svg)](https://pypi.python.org/pypi/jawaf/)
[![PyPI Version](https://img.shields.io/pypi/pyversions/jawaf.svg)](https://pypi.python.org/pypi/jawaf/)

**Jawaf asynchronous web application framework**

What if there was a web framework like [Django](https://www.djangoproject.com/) that was:

* Asynchronous & Non Blocking
* Blazing Fast
* Built on SQLAlchemy Core?

That's the motivation behind Jawaf.

[Sanic](https://github.com/channelcat/sanic) is a blazing fast Python 3.5+ async, non-blocking framework. Jawaf wraps it in a way that makes Django developers feel right at home.
It features built in sessions, async database connectivity through SQLAlchemy Core (with data migrations handled by Alembic), and built in unit testing using py.test. Jawaf also provides management commands, project/app scaffolding, built in CSRF protection, user auth, and an optional RESTful admin API. It's event extensible using simply structured python packages as apps.

Read the [documentation](http://jawaf.readthedocs.io) to get started.

### Built Using

***Core***

[Python 3](https://www.python.org/) (Version 3.6+ Required)

[Sanic](https://github.com/channelcat/sanic)

***Data***

[Alembic](http://alembic.zzzcomputing.com/en/latest/)

[asyncpg](https://github.com/MagicStack/asyncpg)

[ascynpgsa](https://github.com/CanopyTax/asyncpgsa)

[PostgreSQL](https://www.postgresql.org/)

[SQLAlchemy Core](http://docs.sqlalchemy.org/en/latest/core/)

***Session***

[asyncio_redis](https://github.com/jonathanslenders/asyncio-redis)

[Redis](https://redis.io/)

[sanic_session](https://github.com/subyraman/sanic_session)

***Tests***

[py.test](http://doc.pytest.org/en/latest/)

### Features

* Built on an async stack (Sanic) to run fast and scale.
* SQLAlchemy Core integration
* Database migrations
* Sessions
* Validators
* Unit testing
* Management commands
* Project/app scaffolding
* Extensible using structured python packages as apps
* CSRF protection baked in
* Interactive shell (using ipython or bpython if either are detected)
* Async SMTP support
* Optionally server static files
* Optional User Authentication, Groups & Permissions built in
* Optional Admin API

### Notes

Many of the software requirements are in beta, alpha, or even pre-alpha status.
You'd be well advised to have a long hard think about using this in production.

Given the early status of this project it is subject to potential backwards-incompatible changes.

Jawaf is provided "at your own risk".
