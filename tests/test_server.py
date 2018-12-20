import pytest
import jawaf.server


def test___init__(test_project, waf):
    """Test basic server initialization"""
    assert waf.name == 'default'
    assert waf.testing is True


def test_get_jawaf(test_project, waf):
    """Test get_jawaf returns the active Jawaf instance."""
    assert jawaf.server.get_jawaf() == waf


def test_get_sanic(test_project, waf):
    """Test get_sanic returns the active Sanic instance."""
    assert jawaf.server.get_sanic() == waf.server


def test_bad_session(test_project):
    from jawaf.conf import settings
    settings['SESSION'] = {'interface': 'cats'}
    _active_instance = jawaf.server._active_instance
    with pytest.raises(Exception) as excinfo:
        jawaf.server.Jawaf(testing=True)
        assert 'cats' in str(excinfo.value)
    jawaf.server._active_instance = _active_instance
