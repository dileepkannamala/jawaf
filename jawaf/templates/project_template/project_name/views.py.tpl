import os
from mako.template import Template
from sanic.response import html
from sanic.views import HTTPMethodView

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

class LoginView(HTTPMethodView):
    async def get(self, request):
        next_url = request.raw_args.get('next', '')
        return html(Template(filename=os.path.join(template_dir, 'login.html')).render(next=next_url))
