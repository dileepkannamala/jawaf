import jawaf.server

def test___init__(test_project, waf):
    """Test basic server initialization"""
    assert waf.name == 'default'
    assert waf.testing == True

def test_get_jawaf(test_project, waf):
    """Test get_jawaf returns the active Jawaf instance."""
    assert jawaf.server.get_jawaf() == waf

def test_get_sanic(test_project, waf):
    """Test get_sanic returns the active Sanic instance."""
    assert jawaf.server.get_sanic() == waf.server