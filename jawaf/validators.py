from jawaf.exceptions import ValidationError


class Validator(object):

    # When overriding Validator, optionally set __table__ to point to
    # the SQLAlchemy Table you wish to validate
    __table__ = None

    def __init__(self, data):
        """Initialize a Validator.
        :param data: Dict. Values to validate.
        """
        self.data = data
        self.cleaned_data = {}
        self.invalidated_data = {}
        self.validated_data = {}
        self.columns = {}
        if self.__table__ is not None:
            for name in self.__table__.columns.keys():
                self.columns[name] = self._stringify_type(
                    self.__table__.columns.get(name).type)

    def _stringify_type(self, sa_type):
        """Internal method to turn SQLAlchemy types to strings
        :param sa_name: SQLAlchemy Type.
        :return: String. Representation of type.
        """
        return str(sa_type).replace('()', '').lower()

    def is_valid(self, raise_exception=False):
        """Clean and Validate data, optionally raising an exception.
        Populates `Validator.cleaned_data` and `Validator.validated_data`
        as well as `Validator.invalidated_data` if invalid data is found.
        :param raise_exception: Boolean. Whether to raise a
        `jawaf.exceptions.ValidationError`
        :return: Boolean. Whether valid.
        """
        for key in self.data:
            clean = getattr(self, f'clean_{key}', None)
            if clean:
                self.cleaned_data[key] = clean(key, self.data[key])
            else:
                self.cleaned_data[key] = self.data[key]
            # Validate method by column name
            validate = getattr(self, f'validate_{key}', None)
            if not validate and self.columns and key in self.columns:
                # Validate method by column type
                validate = getattr(self, f'validate_{self.columns[key]}', None)
            if validate:
                if not validate(self.cleaned_data[key]):
                    self.invalidated_data[key] = self.cleaned_data[key]
                else:
                    self.validated_data[key] = self.cleaned_data[key]
            else:
                # For now - valid by default if there's no way to check.
                self.validated_data[key] = self.cleaned_data[key]
        if self.invalidated_data and raise_exception:
            raise ValidationError(
                'Validation Failed', self.invalidated_data.keys())
        elif self.invalidated_data:
            return False
        return True

    def validate_integer(self, value):
        """Validate the key value pair.
        :param value: Object.
        :return: True or False depending on validation.
        """
        return isinstance(value, int)

    def validate_text(self, value):
        """Validate the key value pair.
        :param value: Object.
        :return: True or False depending on validation.
        """
        return isinstance(value, str)
