Jawaf
=====

**NOTE: This project is no longer active. I may end up deleting it, but am leaving it up for now.**

|Build Status| |Documentation| |PyPI| |PyPI Version|

**Jawaf asynchronous web application framework**

What if there was a web framework like `Django`_ that was:

-  Asynchronous & Non Blocking
-  Blazing Fast
-  Built on SQLAlchemy Core

That’s the motivation behind Jawaf.

`Sanic`_ is a blazing fast Python 3.5+ async, non-blocking framework.
Jawaf wraps it with Django like functionality. It features built in
sessions, async database connectivity through SQLAlchemy Core (with data
migrations handled by Alembic), and built in unit testing using py.test.
Jawaf also provides management commands, project/app scaffolding, built
in CSRF protection, user auth, and an optional RESTful admin API. It’s
event extensible using simply structured python packages as apps.

Read the `documentation`_ to get started.

**Built On**

`Python 3`_ (Version 3.6+ Required)

`Sanic`_

`Alembic`_

`asyncpg`_

`ascynpgsa`_

`SQLAlchemy Core`_

`sanic\_session`_

`py.test`_

**Features**

-  Built on an async stack (Sanic) to run fast and scale.
-  SQLAlchemy Core integration
-  Database migrations (via Alembic)
-  Sessions (via sanic_session)
-  Validators
-  Unit testing (via py.test)
-  Management commands
-  Project/app scaffolding
-  Extensible using structured python packages as apps
-  CSRF protection baked in
-  Send email asynchronously
-  Optional User Authentication, Groups & Permissions built in
-  Optional Admin API

**Notes**

Many of the software requirements are in beta, alpha, or even pre-alpha
status. You’d be well advised to have a long hard think about using this
in production.

Given the early status of this project it is subject to potential
backwards-incompatible changes.

Jawaf is provided “at your own risk”.

.. _Django: https://www.djangoproject.com/
.. _Sanic: https://github.com/channelcat/sanic
.. _documentation: http://jawaf.readthedocs.io
.. _Python 3: https://www.python.org/
.. _Alembic: http://alembic.zzzcomputing.com/en/latest/
.. _asyncpg: https://github.com/MagicStack/asyncpg
.. _ascynpgsa: https://github.com/CanopyTax/asyncpgsa
.. _SQLAlchemy Core: http://docs.sqlalchemy.org/en/latest/core/
.. _Redis: https://redis.io/
.. _sanic\_session: https://github.com/subyraman/sanic_session
.. _py.test: http://doc.pytest.org/en/latest/

.. |Build Status| image:: https://travis-ci.org/danpozmanter/jawaf.svg?branch=master
   :target: https://travis-ci.org/danpozmanter/jawaf
.. |Documentation| image:: https://readthedocs.org/projects/jawaf/badge/?version=latest
   :target: http://jawaf.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/jawaf.svg
   :target: https://pypi.python.org/pypi/jawaf/
.. |PyPI Version| image:: https://img.shields.io/pypi/pyversions/jawaf.svg
   :target: https://pypi.python.org/pypi/jawaf/
