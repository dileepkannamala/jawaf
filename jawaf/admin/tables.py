from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, Sequence, Table, Text
import jawaf.auth.tables
from jawaf.conf import settings

metadata = MetaData()

audit_action = Table('admin_audit_action', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text()),
    Column('table', Text()),
    Column('target', Text()),
    Column('user_id', Integer, ForeignKey(jawaf.auth.tables.user.c.id), nullable=False),
    Column('username', Text()),
    Column('timestamp', DateTime(timezone=True)), 
    )

DATABASE = settings.ADMIN_CONFIG['database']