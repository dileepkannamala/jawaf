from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, Sequence, Table, Text

metadata = MetaData()

group = Table('auth_group', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text()),
    )

group_permission = Table('auth_group_permission', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer, ForeignKey('auth_group.id'), nullable=False),
    Column('permission_id', Integer, ForeignKey('auth_permission.id'), nullable=False),
    )

permission = Table('auth_permission', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text()),
    Column('target', Text()),
    )

user = Table('auth_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', Text()),
    Column('password', Text()),
    Column('first_name', Text(), nullable=True),
    Column('last_name', Text(), nullable=True),
    Column('email', Text(), nullable=True),
    Column('user_type', Text(), nullable=True),
    Column('is_active', Boolean()),
    Column('is_staff', Boolean()),
    Column('is_superuser', Boolean()),
    Column('date_joined', DateTime(timezone=True)), 
    Column('last_login', DateTime(timezone=True)),
    )

user_group = Table('auth_user_group', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_id', Integer, ForeignKey('auth_group.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('auth_user.id'), nullable=False),
    )

user_password_reset = Table('auth_user_password_reset', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('auth_user.id'), nullable=False),
    Column('selector', Text()),
    Column('verifier', Text()),
    Column('expires', DateTime(timezone=True)), 
    )