import pytest
from jawaf.conf import settings
from jawaf.server import get_jawaf

@pytest.fixture(scope='session')
def waf():
    """Session scoped pytest fixture to provide jawaf instance."""
    instance = get_jawaf(testing=True)
    return instance

# Example test:
#
# def test_view(waf):
#    """Example test to check a hello world view.
#    :param waf: jawaf instance.
#    """
#    request, response = waf.server.test_client.get('/hello_world/')
#    assert 'hello' in response.content
