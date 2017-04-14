import os
from jawaf.conf import settings
from jawaf.management.base import BaseCommand
from jawaf.server import Jawaf

class Command(BaseCommand):
    """Run Jawaf"""

    def add_arguments(self, parser):
        parser.add_argument('--host', help='Server host')
        parser.add_argument('--port', help='Server port')
        parser.add_argument('--debug', help='Debug Mode')
        parser.add_argument('--workers', help='Workers')

    def handle(self, **options):
        print('... Starting Jawaf ...')
        waf = Jawaf(settings.PROJECT_NAME)
        # Optionally override settings with command line options:
        host = options['host'] if options['host'] else settings.HOST
        port = options['port'] if options['port'] else settings.PORT
        debug = (options['debug'].lower() == 'true') if options['debug'] else settings.DEBUG
        workers = int(options['workers']) if options['workers'] else settings.WORKERS
        # Run the server
        waf.run(host=host, port=port, debug=debug, workers=workers)
