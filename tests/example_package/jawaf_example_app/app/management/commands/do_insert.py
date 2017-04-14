import datetime
from jawaf.db import get_engine
from jawaf.conf import settings
from jawaf.management.base import BaseCommand
from jawaf_example_app.app.tables import question

class Command(BaseCommand):

    def handle(self, **options):
        engine = get_engine()
        with engine.connect() as con:
            stmt = question.insert().values(
                question_text='What?', 
                pub_date=datetime.datetime.now())
            con.execute(stmt)
