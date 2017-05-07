import functools
from importlib import import_module
import importlib.util
import os
import sys
from jawaf import __dir__
from jawaf.conf import settings
from jawaf.exceptions import ManagementError

@functools.lru_cache(maxsize=None)
def discover():
    """Discover management commands in the jiwaf core and in the active application.

    :return: List of commands to run.
    """
    # TODO: Look for duplicate commands
    commands = {}
    paths = [settings.BASE_DIR, __dir__]
    for app in settings.INSTALLED_APPS:
        if not 'jawaf.' in app:
            try:
                module = __import__(app)
                paths.append(module.__path__._path[0])
            except:
                pass
    for path in set(paths):
        commands.update(get_commands_in_app(path))
        for filename in os.listdir(path):
            fpath = os.path.join(path, filename)
            if os.path.isdir(fpath):
                commands.update(get_commands_in_app(fpath))
    return commands

def get_commands_in_app(path):
    """Get commands (leaving out any files that start with an underscore).

    :param path: Path to check.
    :return: List of commands if found, or an empty list.
    """
    commands = {}
    app = os.path.split(path)[1]
    path = os.path.join(path, 'management', 'commands')
    if not os.path.exists(path):
        return commands
    for filename in os.listdir(path):
        if filename[0] != '_':
            name = os.path.splitext(filename)[0]
            commands[name] = {'path': path, 'app':app, 'name': name}
    return commands

def execute_from_command_line():
    """Discovers management commands and runs them."""
    commands = discover()
    args = sys.argv[:]
    try:
        command = args[1]
        command = command.replace('-', '_')
    except IndexError:
        # No argument? Display help.
        command = 'help'
    if not command in commands:
        command = 'help'
    if command == 'help':
        args = args[:2]
    run_command(commands[command], args)

def load_command_class(command):
    """Load module and Command class instance from app/name pairing.
    :param command: Dict. App name and command name.
    :return: Instance of named management command in target app.
    """
    command_import = os.path.join(command['path'], '{0}.py'.format(command['name']))
    command_spec = importlib.util.spec_from_file_location('{0}.management.commands.{1}'.format(command['app'], command['name']), command_import)
    if not command_spec:
        raise ManagementError(f'Error processing command file: {command_import}')
    module = importlib.util.module_from_spec(command_spec)
    command_spec.loader.exec_module(module)
    return module.Command()

def run_command(command, args):
    """Run a discovered command.
    :param command: Dict. Contains app name and command name.
    :param args: List. Command line arguments.
    """
    # Load the module and instantiate the class.
    command = load_command_class(command)
    parser = command.create_parser(args[0], args[1])
    command.add_arguments(parser)
    if len(args) > 2:
        args = args[2:]
    else:
        args = []
    # Run with command line arguments
    known, unknown = parser.parse_known_args(args)
    known = vars(known)
    known['unknown'] = unknown
    command.execute(**known)
