import os
from sanic.response import json, text
from sanic.views import HTTPMethodView
import sqlalchemy as sa
from jawaf.admin import registry
from jawaf.auth.decorators import login_required
from jawaf.conf import settings
from jawaf.db import Connection
from jawaf.security import check_headers
from jawaf.server import get_jawaf

class DataView(HTTPMethodView):
    """Endpoint to handle table CRUD."""
    
    async def delete(self, request, table_name):
        if not check_headers(request.headers):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        target_id = request.json.get('id', None)
        if not target_id:
            return json({'message': 'no id'}, status=400)
        async with Connection(table['database']) as con:
            stmt = table['table'].delete().where(table['table'].c.id==target_id)
            await con.execute(stmt)
            return json({'message': 'success'}, status=200)
        return json({'message': 'access denied'}, status=403)
    
    async def get(self, request, table_name):
        waf = get_jawaf()
        table = registry.get(table_name)
        try:
            target_id = int(request.raw_args.get('id', None))
        except:
            return json({'message': 'no id'}, status=400)
        async with Connection(table['database']) as con:
            stmt = sa.select('*').select_from(table['table']).where(table['table'].c.id==target_id)
            result = await con.fetchrow(stmt)
            return json({'message': 'success', 'data': result}, status=200)
        return json({'message': 'access denied'}, status=403)
    
    async def post(self, request, table_name):
        if not check_headers(request.headers):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        async with Connection(table['database']) as con:
            stmt = table['table'].insert().values(**request.json)
            await con.execute(stmt)
            return json({'message': 'success'}, status=201)
        return json({'message': 'access denied'}, status=403)
    
    async def put(self, request, table_name):
        if not check_headers(request.headers):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        target_id = request.json.get('id', None)
        if not target_id:
            return json({'message': 'no id'}, status=400)
        request.json.pop('id')
        async with Connection(table['database']) as con:
            stmt = table['table'].update().where(table['table'].c.id==target_id).values(**request.json)
            await con.execute(stmt)
            return json({'message': 'success'}, status=200)
        return json({'message': 'access denied'}, status=403)

class SearchView(HTTPMethodView):
    """Endpoint to handle searching table data."""

    async def get(self, request, table_name):
        #TODO: Implement This
        return json({'message': 'no data', 'results': ''}, status=401)
