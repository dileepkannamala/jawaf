from jawaf.exceptions import ServerError


async def create_pool(**connection_settings):
    """Create a pool using the `engine` to call the right db backend.
    :param connection_settings: Kwargs.
    :return: Pool.
    """
    engine = connection_settings.pop('engine')
    if engine == 'postgresql':
        from jawaf.adapters.db.postgresql import PostgreSQLBackend
        return await PostgreSQLBackend().create_pool(**connection_settings)
    raise ServerError(f'Unsupported DB Backend {engine}')
