from jawaf.conf import settings

class AdminRegistry(object):
    def __init__(self):
        self._registry = {}

    def get(self, name):
        if not name in self._registry:
            return None
        return self._registry[name]

    def register(self, name, table, database=None):
        self._registry[name] = {'table': table, 'database': database}

registry = AdminRegistry()
def initialize(waf):
    global registry
    if 'jawaf.auth' in settings.INSTALLED_APPS:
        from jawaf.auth.tables import user
        registry.register('user', user, settings.AUTH_CONFIG['database'])

