import pytest
from jawaf.exceptions import ValidationError
from jawaf.validators import Validator
from jawaf.auth.tables import user

class UserValidator(Validator):
    __table__ = user

@pytest.fixture
def validator_data():
    return {
        'id': 1,
        'username': 'test',
    }


def test_validator_is_valid(validator_data):
    data = {
        'id': 1,
        'username': 'test',
        'is_superuser': True,
    }
    v = UserValidator(data=data)
    assert v.is_valid()
    assert 'username' in v.cleaned_data
    assert 'username' in v.validated_data

def test_validator_is_valid_invalid_data(validator_data):
    data = {
        'id': '1',
        'username': 234,
    }
    v = UserValidator(data=data)
    assert not v.is_valid()
    assert 'username' in v.invalidated_data

def test_validator_is_valid_invalid_data_raise_exception(validator_data):
    data = {
        'id': '1',
        'username': 234,
    }
    v = UserValidator(data=data)
    with pytest.raises(ValidationError) as excinfo:
        v.is_valid(raise_exception=True)
        assert 'username' in v.invalidated_data