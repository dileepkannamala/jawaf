from jawaf.db import Connection
from sanic.response import text
from sanic.views import HTTPMethodView
import sqlalchemy as sa
from jawaf_example_app.tables import question

async def query(request):
    query = sa.select('*').select_from(question)
    results = 'Questions:\n'
    async with Connection() as con:
        row = await con.fetchrow(query)
        results += f'{row}\n'
    return text(results)
