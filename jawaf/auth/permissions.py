import sqlalchemy as sa
from jawaf.auth.tables import group, group_permission, permission, user, user_group
from jawaf.auth.utils import database_key
from jawaf.db import Connection

ACCESS_TYPES = {
    'readonly': ['get'],
    'create': ['get', 'post'],
    'edit': ['get', 'post', 'put'],
    'admin': ['delete', 'get', 'post', 'put'],
}

async def add_user_to_group(user_row, group_id):
    database = database_key(database)
    with Connection(database) as con:
        stmt = user_group.insert().values(
            user_id=user_row.id,
            group_id=group_id
            )
        con.execute(stmt)

def add_user_to_group_sync(engine, user_row, group_id):
    with engine.connect() as con:
        stmt = user_group.insert().values(
            user_id=user_row.id,
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
    if user_row.is_superuser:
        return True
    database = database_key(database)
    async with Connection(database) as con:
        query = sa.select('*').select_from(user_group).where(user_group.c.user_id==user_row.id)
        rows = await con.fetch(query)
        group_ids = [row.group_id for row in rows]
        if not group_ids:
            return False
        query = sa.select('*').select_from(group_permission).where(group_permission.c.group_id.in_(group_ids))        
        rows = await con.fetch(query)
        permission_ids = [row.permission_id for row in rows]
        if not permission_ids:
            return False
        query = sa.select('*').select_from(permission) \
            .where(permission.c.id.in_(permission_ids)) \
            .where(permission.c.name==name) \
            .where(permission.c.target==target)
        row = await con.fetchrow(query)
        if row:
            return True
    return False

async def create_group(name, access_type, targets=[], database=None):
    database = database_key(database)  
    permission_names = ACCESS_TYPES[access_type]
    async with Connection(database) as con:
        stmt = group.insert().values(
            name=name,
            )
        grp = await con.execute(stmt)
        perms = []
        for permission_name in permission_names:
            for target in targets:
                stmt = permission.insert().values(
                    name=permission_name,
                    target=target,
                    )
                perms.append(await con.execute(stmt))
        for perm in perms:
            stmt = group_permission.insert().values(
                    permission_id=perm.inserted_primary_key[0],
                    group_id=grp.inserted_primary_key[0]
                )
            await con.execute(stmt)
    return grp.inserted_primary_key[0]

def create_group_sync(engine, name, access_type, targets=[]):
    permission_names = ACCESS_TYPES[access_type]
    with engine.connect() as con:
        stmt = group.insert().values(
            name=name,
            )
        grp = con.execute(stmt)
        perms = []
        for permission_name in permission_names:
            for target in targets:
                stmt = permission.insert().values(
                    name=permission_name,
                    target=target,
                    )
                perms.append(con.execute(stmt))
        for perm in perms:
            stmt = group_permission.insert().values(
                    permission_id=perm.inserted_primary_key[0],
                    group_id=grp.inserted_primary_key[0]
                )
            con.execute(stmt)
    return grp.inserted_primary_key[0]