import sqlalchemy as sa
from jawaf.auth.tables import group, group_permission, permission, user_group
from jawaf.auth.utils import database_key
from jawaf.db import Connection


async def add_user_to_group(user_id, group_id, database=None):
    """Add user to group
    :param user_id: Int. User id to add.
    :param group_id: Int. Group id to add user to.
    :param database: String. Database id to use, or default for AUTH.
    """
    database = database_key(database)
    async with Connection(database) as con:
        stmt = user_group.insert().values(
            user_id=user_id,
            group_id=group_id
            )
        await con.execute(stmt)


def add_user_to_group_sync(engine, user_id, group_id):
    """Add user to group synchronously
    :param engine: SQLAlchemy Engine.
    :param user_id: Int. User id to add.
    :param group_id: Int. Group id to add user to.
    """
    with engine.connect() as con:
        stmt = user_group.insert().values(
            user_id=user_id,
            group_id=group_id
            )
        con.execute(stmt)


async def check_permission(user_row, name, target, database=None):
    """Check permission via groups.
    :param user_row: SQLAlchemy Record. User row to check.
    :param name: String. Name of permission.
    :param target: String. Target for permission (eg a table).
    :return: Boolean. If user has permission on target.
    """
    # TODO: Clean this up.
    if user_row.get('is_superuser'):
        return True
    database = database_key(database)
    async with Connection(database) as con:
        query = sa.select('*').select_from(user_group).where(
            user_group.c.user_id == user_row.get('id'))
        rows = await con.fetch(query)
        group_ids = [row.get('group_id') for row in rows]
        if not group_ids:
            return False
        query = sa.select('*').select_from(group_permission).where(
            group_permission.c.group_id.in_(group_ids))
        rows = await con.fetch(query)
        permission_ids = [row.get('permission_id') for row in rows]
        if not permission_ids:
            return False
        query = sa.select('*').select_from(permission) \
            .where(permission.c.id.in_(permission_ids)) \
            .where(permission.c.name == name) \
            .where(permission.c.target == target)
        row = await con.fetchrow(query)
        if row:
            return True
    return False


async def create_group(name, permission_pairs, database=None):
    """Create a group with specified permissions on targets, plus all join tables.
    :param name: Group name.
    :param permission_pairs: Tuple. List of permission names/targets to create.
    :param database: String. Database id to use, or default for AUTH.
    :return: Int. Group id created.
    """
    database = database_key(database)
    async with Connection(database) as con:
        stmt = group.insert().values(name=name)
        await con.execute(stmt)
        query = sa.select('*').select_from(group).where(
            group.c.name == name).order_by(group.c.id.desc())
        grp = await con.fetchrow(query)
        perms = []
        for permission_pair in permission_pairs:
            stmt = permission.insert().values(**permission_pair)
            await con.execute(stmt)
            query = sa.select('*').select_from(permission).order_by(
                permission.c.id.desc())
            perm = await con.fetchrow(query)
            perms.append(perm)
        for perm in perms:
            stmt = group_permission.insert().values(
                    permission_id=perm.get('id'),
                    group_id=grp.get('id')
                )
            await con.execute(stmt)
    return grp.get('id')


def create_group_sync(engine, name, permission_pairs):
    """Create a group with specified permissions on targets, plus all join tables.
    :param engine: SQLAlchemy Engine. Database engine to connect through.
    :param name: Group name.
    :param permission_pairs: Tuple. List of permission names/targets to create.
    :return: Int. Group id created.
    """
    with engine.connect() as con:
        stmt = group.insert().values(
            name=name,
            )
        grp = con.execute(stmt)
        perms = []
        for permission_pair in permission_pairs:
            stmt = permission.insert().values(**permission_pair)
            perms.append(con.execute(stmt))
        for perm in perms:
            stmt = group_permission.insert().values(
                    permission_id=perm.inserted_primary_key[0],
                    group_id=grp.inserted_primary_key[0]
                )
            con.execute(stmt)
    return grp.inserted_primary_key[0]
