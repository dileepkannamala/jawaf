from importlib import import_module
import importlib.util
import os
from jawaf.server import get_jawaf
from jawaf.conf import settings
from sqlalchemy import create_engine, Table

def create_tables(apps, warn=True):
    """Create tables for each app in a jawaf project.
    :param apps: List. App names to process.
    :param warn: Boolean. Warn before creating tables.
    """
    for app in apps:
        # First try to import the app as a package.
        try:
            module = import_module('%s.tables' % app)
        except ImportError:
            module = None
        # If that didn't work, try importing it from the project.
        if module == None:
            tables_file = os.path.join(settings.BASE_DIR, app, 'tables.py')
            tables_spec = importlib.util.spec_from_file_location('%s.tables' % app, tables_file)
            if not tables_spec:
                module = None
            else:
                module = importlib.util.module_from_spec(tables_spec)
                tables_spec.loader.exec_module(module)
        database_key = getattr(module, 'DATABASE', settings.DEFAULT_DATABASE_KEY)
        if not database_key in settings.DATABASES:
            raise Exception('Database "%s" not found for app %s' % (database_key, app))
        engine = get_engine(database_key)
        if module:
            for item in dir(module):
                attr = getattr(module, item)
                if type(attr) == Table:
                    if warn and engine.dialect.has_table(engine, attr):
                        print('Warning, table %s already exists!' % attr)
                        # TODO: Optionally drop table
            if warn:
                proceed = input('Create Tables (y/n)? ')
                if proceed.lower() == 'n':
                    return
        print('Creating tables for app %s...' % app)        
        module.metadata.create_all(engine)

class Connection:
    """Manage database connections."""

    def __init__(self, database=None, server=None):
        """Initialize
        :param database: String. Database name to connect to. (Default: settings.DEFAULT_DATABASE_KEY)
        :param server: jawaf instance.
        """
        if not server:
            server = get_jawaf()
        if not database:
            database = settings.DEFAULT_DATABASE_KEY
        self.server = server
        self.database = database

    async def __aenter__(self):
        self.con = await self.server.connection(database=self.database)
        return self.con

    async def __aexit__(self, exc_type, exc, tb):
        await self.server.release(self.con, database=self.database)

def get_engine(database=None):
    """Convenience wrapper for SQLAlchemy get_engine.
    :param database: String. Database name from settings.DATABASES to get connection settings from.
    """
    if not database:
        database = settings.DEFAULT_DATABASE_KEY
    connection_settings = settings.DATABASES[database]
    return create_engine('%(engine)s://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % connection_settings)
