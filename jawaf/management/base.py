from argparse import ArgumentParser
from importlib import import_module
from fnmatch import fnmatch
import os
from mako.template import Template
from jawaf import __dir__, __version__

### Some spicy goodness from Django with edits

class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.
    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.
    """
    pass

class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        raise CommandError("Error: %s" % message)

### /Some spicy goodness from Django

class BaseCommand(object):
    """Base management command class."""

    ### More Django with some edits
    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.

        :param prog_name: String. Program name.
        :param subcommand: String. subcommand.
        """
        parser = CommandParser(
            self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=None,
        )
        return parser
    ### / More Django

    def add_arguments(self, parser):
        """Override in subclasses to add arguments to the parser."""
        pass

    def execute(self, **options):
        """Wrap the call to handle in case we want to do any setup like Django does in the future.

        :param options: Dictionary of argparse options.
        """
        self.handle(**options)

    def handle(self, **options):
        """Override in subclasses

        Doesn't replicate legacy optparse behavior. Positional arguments if present are
        in the `args` key in **options.

        :param options: Dictionary of argparse options.
        """
        pass

class TemplateCommand(BaseCommand):
    """Base management command class for jawaf template commands (start-project and start-app)."""

    def __init__(self):
        """Initialize command with general purpose variables such as 'version'."""
        super(BaseCommand, self).__init__()
        self.variables = {'version': __version__, 'next': '${next}'}

    def add_arguments(self, parser):
        """ArgParse add_arguments override to add `name` and `directory` options.
        :param parser: ArgParse parser.
        """
        parser.add_argument('name', help='Name of the application or project.')
        parser.add_argument('--directory', help='Optional destination directory')

    def handle(self, **options):
        """Called when command executes. 
        Generates variables to pass into template and then renders the templates.
        :param options: kwargs. Options passed in from execution of command.
        """
        template = options.pop('template')
        target_base_dir = options.pop('directory')
        if not target_base_dir:
            target_base_dir = os.getcwd()
        target_name = options.pop('name')
        if template == 'project_template':
            self.variables['project_name'] = target_name
            self.variables['secret_key'] = options.pop('secret_key')
        elif template == 'app_template':
            self.variables['project_name'] = os.path.split(target_base_dir)[1]
            self.variables['app_name'] = target_name
        try:
            import_module(target_name)
        except ImportError:
            pass
        else:
            raise CommandError('%s conflicts with an existing module. Please try another name.' % target_name)
        template_dir = os.path.join(__dir__, 'templates', template)
        self._render(target_name, template_dir, os.path.join(target_base_dir, target_name))

    def _render(self, target_name, read_path, write_path):
        """Render a given template or directory for the target.
        :param target_name: String. Project or App name to render.
        :param read_path: String. Path to template or directory to render.
        :param write_path: String. Path to write to (or create directory).
        """
        if os.path.isdir(read_path):
            if os.path.split(read_path)[1] == 'project_name':
                write_path = os.path.join(os.path.split(write_path)[0], self.variables['project_name'])
            os.mkdir(write_path)
            for filename in os.listdir(read_path):
                if fnmatch(filename, 'test_*'):
                    write_filename = filename.replace('test_', 'test_%s_' % target_name)
                else:
                    write_filename = filename
                self._render(target_name, os.path.join(read_path, filename), os.path.join(write_path, write_filename))
        else:
            tpl = Template(filename=read_path)
            with open(os.path.splitext(write_path)[0], 'w') as f:
                f.write(tpl.render(**self.variables))
