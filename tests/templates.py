project_routes = '''
from test_project.test_app.views import login # Quick login hack for testing purposes
routes = [
    {'uri': '/login/', 'handler': login},
    {'uri': '/test_app/', 'include': 'test_app'},
    {'uri': '/auth/', 'include': 'jawaf.auth'},
    {'uri': '/example_app/', 'include': 'jawaf_example_app'},
]
'''

app_routes = '''from test_project.test_app.views import hello, protected

routes = [
    {'uri': 'hello/', 'handler': hello},
    {'uri': 'protected/', 'handler': protected},
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
from jawaf.auth.decorators import login_required

async def hello(request):
    return text('Hello!')

@login_required
async def protected(request):
    return text('Protected!')

async def login(request):
    return text('login')
'''

def edit_settings(settings_path, target, new_string):
    data = ''
    with open(settings_path, 'r') as f:
        data = f.read()
    data = data.replace(target, new_string)
    with open(settings_path, 'w') as f:
        data = f.write(data)

def write_template(name, path):
    with open(path, 'w') as f:
        f.write(globals()[name])