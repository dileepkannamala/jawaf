import asyncpgsa

class PostgreSQLBackend(object):
    """Adapter for async Postgresql database backend."""

    async def create_pool(self, *args, **kwargs):
        """Wrap asyncpgsa create_pool."""
        return await asyncpgsa.create_pool(*args, **kwargs)