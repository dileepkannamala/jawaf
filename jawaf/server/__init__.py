import fnmatch
from importlib import import_module
import importlib.util
import os
from smtplibaio import SMTP
from sanic import Blueprint, Sanic
from sanic_session import InMemorySessionInterface, RedisSessionInterface
from jawaf.conf import settings
from jawaf.security import generate_csrf_token

# Active instance of Jawaf (singleton)
_active_instance = None

class Jawaf(object):
    """Wraps a Sanic instance (server), and manages db connection pools, sanic routes, and the session."""

    def __init__(self, name='default', testing=False):
        """Initialize Jawaf instance. Set up routes, database connections, and session.
        :param name: String. Sanic instance name. (Default: 'default')
        :param testing: Boolean. Whether or not testing framework is active.
        """
        self.name = name
        self.server = Sanic(name)
        self.testing = testing

        self._db_pools = {}
        self._session_pool = None
        self._smtp = None
        global _active_instance
        _active_instance = self

        self.add_routes(routes_import=os.path.join(settings.PROJECT_DIR, 'routes.py'), base_path=settings.BASE_DIR)
        self.init_databases()
        self.init_session()
        self.init_smtp()
        self.init_apps()

    def add_route(self, *args, **options):
        """Wraps Sanic.add_route"""
        self.server.add_route(*args, **options)

    def add_websocket_route(self, *args, **options):
        """Wraps Sanic.add_websocket_route"""
        self.server.add_websocket_route(*args, **options)

    def add_routes(self, routes_import, base_path, prefix=''):
        """Recursively add routes using routes.py files.
        :param routes_import: String. Relative path to the routes.py file to parse.
        :param base_path: String. Base path for the jawaf project.
        :param prefix: String. Prefix url path (for recursion) - passed in via include directives.
        """
        try:
            if routes_import[0] == '/':
                module = import_module(os.path.splitext(routes_import)[0])
            else:
                module = import_module(routes_import)
        except ImportError:
            module = None
        if module == None:
            routes_spec = importlib.util.spec_from_file_location(f'{self.name}{prefix}.routes', routes_import)
            if not routes_spec:
                raise Exception(f'Error processing routes file: {routes_import}')
            module = importlib.util.module_from_spec(routes_spec)
            routes_spec.loader.exec_module(module)
        for route in module.routes:
            if prefix:
                route['uri'] = ''.join([prefix, route['uri']])
            if 'include' in route:
                try:
                    import_module(route['include'])
                    # Treat as a package
                    self.add_routes('.'.join([route['include'], 'routes']), base_path=base_path, prefix=route['uri'])
                except ImportError:
                    # Treat as a relative path
                    self.add_routes(os.path.join(base_path, route['include'], 'routes.py'), base_path=base_path, prefix=route['uri'])
            elif 'websocket' in route and route['websocket'] == True:
                self.add_websocket_route(**route)
            else:
                self.add_route(**route)

    async def close_database_pools(self):
        """Asynchronously close all open database connection pools."""
        for database in self._db_pools:
            await self._db_pools[database].close()

    async def connection(self, database=None):
        """Asynchronously return a connection from the named database connection pool.
        :param database: String. Name of the database key in settings.py to call. (Default: settings.DEFAULT_DATABASE_KEY)
        """
        if not database:
            database = settings.DEFAULT_DATABASE_KEY
        return await self._db_pools[database].acquire()

    async def create_database_pool(self, database=None):
        """Create the database pool for the specified database. Used for unit tests, handled by Sanic blueprint when server is running.
        :param database: String. Name of the database key in settings.py to call. (Default: settings.DEFAULT_DATABASE_KEY)
        """
        if not database:
            database = settings.DEFAULT_DATABASE_KEY
        from jawaf.conf import settings
        connection_settings = settings.DATABASES[database].copy()
        connection_settings.pop('engine') # Pop out engine before passing it into the create_pool method on the db backend.
        self._db_pools[database] = await settings.DB_BACKEND.create_pool(**connection_settings)

    async def get_session_pool(self):
        """Asynchronously return a connection from the session connection pool."""
        if not self._session_pool:
            self._session_pool = await asyncio_redis.Pool.create(**settings.SESSION)
        return self._session_pool

    def get_smtp(self):
        return self._smtp

    def init_apps(self):
        """Run any initialization code inside an app"""
        for app in settings.INSTALLED_APPS:
            try:
                module = import_module(app)
            except ImportError:
                app_import = os.path.join(settings.BASE_DIR, app)
                app_spec = importlib.util.spec_from_file_location(f'app.{app}', app_import)
                if app_spec:
                    module = importlib.util.module_from_spec(app_spec)
                    app_spec.loader.exec_module(module)
            if module:
                if hasattr(module, 'initialize'):
                    module.initialize(self)

    def init_databases(self):
        """Initialize database connection pools from settings.py, 
        setting up Sanic blueprints for server start and stop."""
        for database in settings.DATABASES:
            db_blueprint = Blueprint(f'{self.name}_db_blueprint_{database}')
            connection_settings = settings.DATABASES[database].copy()
            connection_settings.pop('engine') # Pop out engine before passing it into the create_pool method on the db backend.
            @db_blueprint.listener('before_server_start')
            async def setup_connection_pool(app, loop):
                self._db_pools[database] = await settings.DB_BACKEND.create_pool(**connection_settings)
            @db_blueprint.listener('after_server_stop')
            async def close_connection_pool(app, loop):
                if database in self._db_pools and self._db_pools[database]:
                    await self._db_pools[database].close()
            self.server.blueprint(db_blueprint)

    def init_session(self):
        """Initialize the session connection pool, using either in memory interface or redis."""
        interface_type = settings.SESSION.pop('interface')
        if self.testing:
            # Set the session to in memory for unit tests.
            # TODO: Revisit this!
            interface_type = 'memory'
        if interface_type == 'memory':
            self._session_interface = InMemorySessionInterface()
        elif interface_type == 'redis':
            self._session_interface = RedisSessionInterface(self.get_session_pool())
        else:
            raise Exception(f'Unexpected session type "{interface}".')
        @self.server.middleware('request')
        async def add_session_to_request(request):
            await self._session_interface.open(request)
            request['session']['csrf_token'] = 'test_token' if self.testing else generate_csrf_token()
        @self.server.middleware('response')
        async def save_session(request, response):
            await self._session_interface.save(request, response)

    def init_smtp(self):
        """Initialize smtp connection"""
        if not 'SMTP' in settings:
            return
        smtp_blueprint = Blueprint(f'{self.name}_smtp_blueprint')
        @smtp_blueprint.listener('before_server_start')
        async def connect_smtp(app, loop):
            self._smtp = SMTP(hostname=settings.SMTP['host'], port=settings.SMTP['port'])
            await self._smtp.connect()
            if 'username' in settings.SMTP and 'password' in settings.SMTP:
                await self._smtp.auth.auth(settings.SMTP['username'], settings.SMTP['password'])
        self.server.blueprint(smtp_blueprint)

    async def release(self, connection, database=None):
        """Asynchronously release a connection to the database specified.
        :param connection: Connection object. Connection to database to release.
        :param database: String. Database name from settings.py"""
        if not database:
            database = settings.DEFAULT_DATABASE_KEY
        await self._db_pools[database].release(connection)

    def run(self, *args, **options):
        """Wrapper for Sanic instance run method."""
        return self.server.run(*args, **options)

def get_jawaf(testing=False):
    """Convenience method to get the active Jawaf instance, or create one if none exists.
    :param test: Boolean. Whether or not the testing framework is active.
    :return: Jawaf Instance (which wraps Sanic instance)
    """
    global _active_instance
    if not _active_instance:
        _active_instance = Jawaf(name=settings.PROJECT_NAME, testing=testing)
    return _active_instance

def get_sanic():
    """Convenience method to get the active Sanic instance via the active Jawaf instance.
    :return: Sanic instance.
    """
    return get_jawaf().server
