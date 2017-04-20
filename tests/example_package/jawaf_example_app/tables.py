from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, Table, Text
from jawaf.admin import registry

metadata = MetaData()

question = Table('example_app_question', metadata,
    Column('id', Integer, primary_key=True),
    Column('question_text', Text()),
    Column('pub_date', DateTime()),
    )

registry.register('question', question, 'default')