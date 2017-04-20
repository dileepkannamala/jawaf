from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, Sequence, Table, Text

metadata = MetaData()

audit_action = Table('admin_audit_action', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Text()),
    Column('table', Text()),
    Column('user_id', Integer, ForeignKey('auth_user.id'), nullable=False),
    Column('username', Text()),
    Column('timestamp', DateTime(timezone=True)), 
    )
