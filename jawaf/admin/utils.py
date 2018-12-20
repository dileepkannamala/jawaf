from jawaf.conf import settings


def database_key(database):
    """Get the default database key for jawaf.auth
    :param database: String. Database name to connect to.
    """
    if not database:
        return settings.ADMIN_CONFIG['database']
    return database
