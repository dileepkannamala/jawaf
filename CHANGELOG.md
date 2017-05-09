# Version 0.3.2
- Convert README from MD to RST

# Version 0.3.1

- Requirements Update
- README Update
- Quick fix to remove *log files created after tests

# Version 0.3.0

- Validators
- Scaffolding to allow flexibility with different db backends
- Refactor
- Static file support
- Custom exceptions

# Version 0.2.3

- Redis session fix
- Minor db refactor
- More tests
- Tweaks to admin and auth views

# Version 0.2.2

- Template fix in manage.py
- Allow connection to db without user/password
- Comment out database settings in settings.py by default
- Make session support optional

# Version 0.2.1

- sys.path fix in manage.py

# Version 0.2.0

- Alembic Migrations
- Support unknown arguments in management commands
- `py.test --args='xs'` -> `py.test -xs`
- Optional SSL support for SMTP
- Additional documentation
- Tightening up manage.py import/structure

# Version 0.1.2

- Async SMTP Support

# Version 0.1.1

- Admin API: put -> patch
- Modern string formatting
- Added sort, limit, offset to admin search

# Version 0.1.0

- Initial release
- Basic structure and core features of server
- Management commands
- New project/app scaffolding
- Basic admin API
- User Auth
- CSRF Protection
- Async Postgresql support
- SQLAlchemy Core support
- Unit tests via py.test