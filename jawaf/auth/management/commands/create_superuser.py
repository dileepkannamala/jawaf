import getpass
import os
from jawaf.auth.users import create_user_from_engine
from jawaf.conf import settings
from jawaf.db import get_engine
from jawaf.management.base import BaseCommand
from jawaf.server import Jawaf

class Command(BaseCommand):
    """Create Super User"""

    def _validate_password(self, password, password2):
        # TODO: Check for short passwords or other rules like mixed case and numbers?
        if password != password2:
            print('Passwords do not match.')
            return False
        if len(password.strip()) == 0:
            print('Passwords cannot be empty.')
            return False
        return True

    def handle(self, **options):
        print('Create a super user')
        waf = Jawaf(settings.PROJECT_NAME)
        username = input('Username: ')
        email = input('Email Address: ')
        engine = get_engine()
        password = None
        while(password == None):
            password = getpass.getpass()
            password2 = getpass.getpass('Password (again): ')
            if not self._validate_password(password, password2):
                password = None
        create_user_from_engine(engine, username=username, password=password, email=email, is_staff=True, is_superuser=True)
