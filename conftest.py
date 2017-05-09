import asyncio
import pytest
import os
import pip
import shutil
import sanic
from sqlalchemy import create_engine
import sys
import testing.postgresql
from tests import templates
sys.path.insert(0, os.path.abspath('jawaf'))

@pytest.fixture(scope='session')
def test_project():
    """Setup a test project, test app, and test app package.
    Load settings and create tables.
    Cleans up when test session ends.
    """
    # Setup test package:
    pip.main(['install', 'tests/example_package/'])
    # Create a test project
    test_dir = 'temp_test'
    test_project = 'test_project'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    from jawaf.management.commands import start_project, start_app
    start_project.Command().handle(name=test_project, directory=os.path.abspath(test_dir))
    os.mkdir(os.path.join(os.path.abspath(test_dir), 'static'))
    start_app.Command().handle(name='test_app', directory=os.path.abspath(os.path.join(test_dir, test_project)))
    # Create the code for the test project
    templates.write_template('project_routes', os.path.abspath(os.path.join(test_dir, test_project, test_project, 'routes.py')))
    templates.write_template('app_routes', os.path.abspath(os.path.join(test_dir, test_project, 'test_app', 'routes.py')))
    templates.write_template('app_views', os.path.abspath(os.path.join(test_dir, test_project, 'test_app', 'views.py')))
    templates.write_template('app_tables', os.path.abspath(os.path.join(test_dir, test_project, 'test_app', 'tables.py')))
    templates.edit_settings(os.path.abspath(os.path.join(test_dir, test_project, test_project, 'settings.py')), 
        targets=[
            ["'jawaf.auth',", "'jawaf.auth',\n    'test_app',\n    'jawaf_example_app',"],
            ['HOST', "SMTP = {'host':'localhost', 'port':8024}\n\nHOST"],
            ["# STATIC", 'STATIC'],
        ])
    # Setup test postgresql
    postgresql = testing.postgresql.Postgresql()
    create_engine(postgresql.url())
    # Hot Patch
    import smtplibaio
    from jawaf.utils.testing import MockSMTP
    smtplibaio.SMTP = MockSMTP
    smtplibaio.SMTP_SSL = MockSMTP
    # Setup Settings and reload modules to ensure the project settings are loaded.
    os.environ.setdefault('JAWAF_SETTINGS_PATH', f'{test_dir}/{test_project}/{test_project}/settings.py')
    sys.path.insert(0, os.path.abspath(test_dir))
    from imp import reload
    from jawaf import conf, db, management, security, server, utils
    import jawaf.auth, jawaf.auth.users, jawaf.auth.utils
    import jawaf.admin, jawaf.admin.utils
    reload(conf)
    reload(db)
    reload(management)
    reload(security)
    reload(server)
    reload(utils)
    reload(jawaf.auth.users)
    reload(jawaf.auth.utils)
    reload(jawaf.admin)
    reload(jawaf.admin.utils)
    from jawaf.conf import settings
    p_dsn = postgresql.dsn()
    settings['DATABASES']['default'] = {'engine':'postgresql'}
    settings['DATABASES']['default']['database'] = p_dsn['database']
    settings['DATABASES']['default']['host'] = p_dsn['host']
    settings['DATABASES']['default']['port'] = p_dsn['port']
    settings['DATABASES']['default']['user'] = p_dsn['user']
    settings['DATABASES']['default']['password'] = ''
    settings['SESSION'] = {'interface': 'memory'}
    # Create tables for auth and the example app
    from jawaf.db import create_tables
    create_tables(['jawaf.auth'], warn=False)
    create_tables(['jawaf.admin'], warn=False)
    create_tables(['jawaf_example_app'], warn=False)
    yield True
    # Clean up
    postgresql.stop()
    shutil.rmtree(test_dir)
    os.remove('access.log')
    os.remove('error.log')
    pip.main(['uninstall', 'jawaf_example_app', '-y'])

@pytest.fixture(scope='session')
def waf():
    """Create a Jawaf instance for test session."""
    import jawaf.server
    return jawaf.server.Jawaf(testing=True)
