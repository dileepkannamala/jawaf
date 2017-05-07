import jawaf.management
import os

def test_discover(test_project, waf):
    """Test basic command discovery."""
    commands = jawaf.management.discover()
    assert 'run' in commands
    assert 'start_project' in commands

def test_execute_from_command_line(test_project, waf):
    """Test execute from command line."""
    commands = jawaf.management.discover()
    import sys
    sys.argv = ['', 'start-app', 'oranges', '--directory=temp_test/test_project']
    jawaf.management.execute_from_command_line()
    assert os.path.exists(os.path.abspath('temp_test/test_project/oranges'))

def test_execute_from_command_line_bad_command(test_project, waf):
    """Test execute from command line with a bad command."""
    commands = jawaf.management.discover()
    import sys
    sys.argv = ['', 'sing-song', 'uhoh', '--directory=temp_test/test_project']
    jawaf.management.execute_from_command_line()
    assert os.path.exists(os.path.abspath('temp_test/test_project/uhoh')) == False

def test_run_command(test_project, waf):
    """Test run command"""
    commands = jawaf.management.discover()
    jawaf.management.run_command(commands['start_app'], ['', '', 'apples', '--directory=temp_test/test_project'])
    assert os.path.exists(os.path.abspath('temp_test/test_project/apples'))