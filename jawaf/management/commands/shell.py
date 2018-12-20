from jawaf.conf import settings
from jawaf.management.base import BaseCommand
from jawaf.server import Jawaf


class Command(BaseCommand):
    """Start jawaf shell"""

    def handle(self, **options):
        print('... starting jawaf shell ...')
        waf = Jawaf(settings.PROJECT_NAME)
        # Use IPython if it exists
        try:
            import IPython
            IPython.embed()
            return
        except ImportError:
            pass
        # Use bypython if it exists
        try:
            import bpython
            bpython.embed()
            return
        except ImportError:
            pass
        # Ok, just do the pumpkin spice python shell.
        import code
        code.interact(local=locals())
