import os
from mako.template import Template
from sanic.response import json, text
from sanic.views import HTTPMethodView
from jawaf.auth.decorators import login_required
from jawaf.auth.users import check_user, log_in, log_out, update_user
from jawaf.conf import settings

class LoginView(HTTPMethodView):
    """Endpoint to handle user login."""
    
    async def post(self, request):
        username = request.form.get('username', '')
        password = request.form.get('password', None)
        next_url = request.form.get('next', None)
        if password is None:
            return json({'message': 'no password'}, status=403)
        user_row = await check_user(username, password)
        if user_row:
            await log_in(request, user_row)
            return json({'message': 'login succeeded', 'next': next, 'username': username}, status=200)
        return json({'message': 'login failed'}, status=403)

class LogoutView(HTTPMethodView):
    """Endpoint to handle user logout."""

    async def post(self, request):
        user_row = request['session'].get('user', None)
        if user_row:
            await log_out(request, user_row)
            return json({'message': 'logout succeeded'}, status=200)
        return json({'message': 'not logged in'}, status=401)

class PasswordChangeView(HTTPMethodView):
    """Endpoint to handle user password change."""

    async def post(self, request):
        username = request.form.get('username', '')
        old_password = request.form.get('old_password', None)
        new_password = request.form.get('new_password', None)
        user_row = await check_user(username, old_password)
        if not user_row:
            return json({'message': 'bad user data'}, status=403)
        if user_row.id != request['session']['user'].id:
            return json({'message': 'bad user data'}, status=403)
        await update_user(database=None, target_username=username, password=new_password)
        return json({'message': 'password changed'}, status=200)

# TODO: Implement Password Reset
class PasswordResetView(HTTPMethodView):
    """Endpoint to handle user password reset."""

    async def post(self, request):
        return json({'message': 'password reset is not yet implemented'}, status=501)