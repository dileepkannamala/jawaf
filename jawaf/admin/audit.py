from jawaf.admin.tables import audit_action
from jawaf.admin.utils import database_key
from jawaf.db import Connection


async def add_audit_action(name, target, table_name, user_row, database=None):
    """Add audit action
    :param name: String. Action name.
    :param target: String. Action target.
    :param table_name: String. Table name.
    :param user_row: SQLAlchemy Record. User row.
    :param database: String. Database id to use, or default for AUTH.
    """
    database = database_key(database)
    async with Connection(database) as con:
        stmt = audit_action.insert().values(
            name=name,
            table=table_name,
            target=target,
            user_id=user_row.get('id'),
            username=user_row.get('username'),
            )
        await con.execute(stmt)

# TODO: Potentially add in convenience methods to clean this table?
