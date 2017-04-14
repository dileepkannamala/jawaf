import jawaf.management

def test_query(test_project, waf):
    """Test an installed app via a python package has been loaded, and the management command runs."""
    commands = jawaf.management.discover()
    jawaf.management.run_command(commands['do_insert'], ['', ''])
    request, response = waf.server.test_client.get('/example_app/query/')
    assert "question_text='What?'" in response.text