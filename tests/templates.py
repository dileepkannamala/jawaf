# Templates used by ../conftest.py to generate the test project, plus two utility methods.

project_routes = '''
from test_project.test_app.views import default, login # Quick view hack for testing purposes
routes = [
    {'uri': '/', 'handler': default},
    {'uri': '/login/', 'handler': login},
    {'uri': '/test_app/', 'include': 'test_app'},
    {'uri': '/auth/', 'include': 'jawaf.auth'},
    {'uri': '/admin/', 'include': 'jawaf.admin'},
    {'uri': '/example_app/', 'include': 'jawaf_example_app'},
]
'''

app_routes = '''from test_project.test_app.views import hello, read_only, protected, protected_403, send_email

routes = [
    {'uri': 'hello/', 'handler': hello},
    {'uri': 'protected/', 'handler': protected},
    {'uri': 'protected_403/', 'handler': protected_403},
    {'uri': 'read_only/', 'handler': read_only},
    {'uri': 'email/', 'handler': send_email, 'methods': ['POST']},
]
'''

app_tables = '''from sqlalchemy import Column, Integer, MetaData, Table, Text

metadata = MetaData()

person = Table('test_app_person', metadata,
   Column('id', Integer, primary_key=True),
   Column('name', Text()),
   )
'''

app_views = '''from sanic.response import text
from jawaf.auth.decorators import has_permission, login_required
from jawaf.mail import send_mail

async def default(request):
    return text('/')

async def hello(request):
    return text('Hello!')

@login_required(redirect=True)
async def protected(request):
    return text('Protected!')

@login_required()
async def protected_403(request):
    return text('Protected!')

@has_permission(name='get', target='test_app')
async def read_only(request):
    return text('Protected!')

async def login(request):
    return text('login')

async def send_email(request):
    await send_mail(subject=request.json.get('subject'),
        message=request.json.get('message'), 
        from_address=request.json.get('from_address'), 
        to=request.json.get('to'), 
        cc=request.json.get('cc', None),
        bcc=request.json.get('bcc', None),
        html_message=request.json.get('html_message', None)
    )
    return text('!')
'''

def edit_settings(settings_path, targets=[]):
    data = ''
    with open(settings_path, 'r') as f:
        data = f.read()
    for target, new_string in targets:
        data = data.replace(target, new_string)
    with open(settings_path, 'w') as f:
        data = f.write(data)

def write_template(name, path):
    with open(path, 'w') as f:
        f.write(globals()[name])