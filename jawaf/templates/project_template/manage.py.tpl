#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ.setdefault(
        'JAWAF_SETTINGS_PATH', f'{base_dir}/${project_name}/settings.py')
    sys.path.insert(0, os.path.dirname(base_dir))
    try:
        from jawaf.management import execute_from_command_line
    except ImportError:
        # Ensure the import is due to jawaf not being found.
        try:
            import jawaf
        except ImportError:
            raise ImportError(
                "Couldn't import jawaf. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
                " Would you like a hug?"
                " I'm sorry Dave, I'm afraid I can't do that."
            )
        raise
    execute_from_command_line()
