
## Jawaf ##

[![Build Status](https://travis-ci.org/danpozmanter/jawaf.svg?branch=master)](https://travis-ci.org/danpozmanter/jawaf)

**Jawaf asynchronous web application framework**

A fast asynchronous web application framework.

Read the [Documentation](http://jawaf.readthedocs.io) to get started.

Inspired by (and using some code/concepts from) [Django](https://www.djangoproject.com/) and the promise of [Sanic](https://github.com/channelcat/sanic).

The goal of this project is to provide much of what Django provides (convenience, smart scaffolding, ease of development) on top an async python 3 core.

**Built Using**

***Core***

[Python 3](https://www.python.org/) (Version 3.6+ Required)

[Sanic](https://github.com/channelcat/sanic)

***Data***

[SQLAlchemy Core](http://docs.sqlalchemy.org/en/latest/core/)

[PostgreSQL](https://www.postgresql.org/)

[asyncpg](https://github.com/MagicStack/asyncpg)

[ascynpgsa](https://github.com/CanopyTax/asyncpgsa)

***Session***

[sanic_session](https://github.com/subyraman/sanic_session)

[asyncio_redis](https://github.com/jonathanslenders/asyncio-redis)

[Redis](https://redis.io/)

***Templating***

[Mako](http://www.makotemplates.org/)

***Tests***

[py.test](http://doc.pytest.org/en/latest/)

**Features**

* Built on an async stack to run fast and scale.
* Built in support for:
    * Database interaction via SQLAlchemy Core
    * Sessions via sanic_session and Redis
    * Unit testing via py.test
    * Django style management commands and project/app scaffolding
    * Interactive shell (using ipython or bpython if either are detected)
    * User Authentication, Groups & Permissions built in

Note: Many of the software requirements are in beta, alpha, or even pre-alpha status.
You'd be well advised to have a long hard think about using this in production.

Given the early status of this project it is subject to potential backwards-incompatible changes.

Jawaf is provided "at your own risk".
