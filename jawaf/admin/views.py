import os
from sanic.response import json, text
from sanic.views import HTTPMethodView
import sqlalchemy as sa
from jawaf.admin import registry
from jawaf.admin.audit import add_audit_action
from jawaf.auth.decorators import has_permission
from jawaf.auth.permissions import add_user_to_group, create_group
from jawaf.conf import settings
from jawaf.db import Connection
from jawaf.security import check_csrf
from jawaf.server import get_jawaf

class DataView(HTTPMethodView):
    """Endpoint to handle table CRUD."""
    
    @has_permission(name='delete', target='admin')
    async def delete(self, request, table_name=None):
        if not check_csrf(request):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        target_id = request.json.get('id', None)
        if not target_id:
            return json({'message': 'no id'}, status=400)
        if not table:
            return json({'message': 'access denied'}, status=403)
        async with Connection(table['database']) as con:
            stmt = table['table'].delete().where(table['table'].c.id==target_id)
            await con.execute(stmt)
        await add_audit_action('delete', 'admin', table_name, request['session']['user'])
        return json({'message': 'success'}, status=200)
    
    @has_permission(name='get', target='admin')
    async def get(self, request, table_name=None):
        waf = get_jawaf()
        table = registry.get(table_name)
        try:
            target_id = int(request.raw_args.get('id', None))
        except:
            return json({'message': 'no id'}, status=400)
        if not table:
            return json({'message': 'access denied'}, status=403)
        async with Connection(table['database']) as con:
            query = sa.select('*').select_from(table['table']).where(table['table'].c.id==target_id)
            result = await con.fetchrow(query)
            return json({'message': 'success', 'data': result}, status=200)
        return json({'message': 'access denied'}, status=403)
    
    @has_permission(name='post', target='admin')
    async def post(self, request, table_name=None):
        if not check_csrf(request):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        if not table:
            return json({'message': 'access denied'}, status=403)
        async with Connection(table['database']) as con:
            stmt = table['table'].insert().values(**request.json)
            await con.execute(stmt)
        await add_audit_action('post', 'admin', table_name, request['session']['user'])
        return json({'message': 'success'}, status=201)
    
    @has_permission(name='put', target='admin')
    async def put(self, request, table_name=None):
        if not check_csrf(request):
            return json({'message': 'access denied'}, status=403)
        waf = get_jawaf()
        table = registry.get(table_name)
        target_id = request.json.get('id', None)
        if not target_id:
            return json({'message': 'no id'}, status=400)
        if not table:
            return json({'message': 'access denied'}, status=403)
        request.json.pop('id')
        async with Connection(table['database']) as con:
            stmt = table['table'].update().where(table['table'].c.id==target_id).values(**request.json)
            await con.execute(stmt)
        await add_audit_action('put', 'admin', table_name, request['session']['user'])
        return json({'message': 'success'}, status=200)

class ManageAccessView(HTTPMethodView):
    """Convenience endpoint for adding/editing users, groups, and permissions."""

    # @has_permission(name='manage_access.delete', target='admin')
    # async def delete(self, request):
    #     # TODO: Implement group and permission deletion in bulk?
    #     return json({'message': 'Not yet implemented'}, status=401)  

    # @has_permission(name='manage_access.get', target='admin')
    # async def get(self, request):
    #     # TODO: Possibly implement bulk return of groups and permissions for a user.
    #     return json({'message': 'Not yet implemented'}, status=401)  

    @has_permission(name='manage_access.post', target='admin')
    async def post(self, request):
        user_ids = request.json.get('user_ids')
        group_name = request.json.get('group_name')
        permission_pairs = request.json.get('permissions')
        group_id = await create_group(group_name, permission_pairs)
        for user_id in user_ids:
            await add_user_to_group(user_id, group_id)
        return json({'message': 'success'}, status=200)

    # @has_permission(name='manage_access.put', target='admin')
    # async def put(self, request):
    #     # TODO: Implement group and permission editing in a bulk fashion?
    #     return json({'message': 'Not yet implemented'}, status=401)    

class SearchView(HTTPMethodView):
    """Endpoint to handle searching table data."""

    @has_permission(name='search.get', target='admin')
    async def get(self, request, table_name=None):
        field = request.raw_args.get('field', '')
        value = request.raw_args.get('value', '')
        waf = get_jawaf()
        table = registry.get(table_name)
        if not table:
            return json({'message': 'access denied'}, status=403)
        if field and value:
            async with Connection(table['database']) as con:
                query = sa.select('*').select_from(table['table']).where(getattr(table['table'].c, field).ilike(value))
                results = await con.fetch(query)
                if results:
                    return json({'message': 'success', 'results': [r for r in results]}, status=200)
        return json({'message': 'no data', 'results': ''}, status=401)
