class ConfigurationError(Exception):
    """Problem with configuration (settings.py)"""
    pass

class ManagementError(Exception):
    """Problem with management commands"""
    pass

class ServerError(Exception):
    """General Purpose Jawaf Error"""
    pass

class ValidationError(Exception):
    """Validation failed"""

    def __init__(self, message, invalidated_fields):
        """Initialize ValidationError
        :param string message: Exception message.
        :param object errors: List of error fields.
        """
        super(ValidationError, self).__init__(f'{message}: {invalidated_fields}')
        self.invalidated_fields = invalidated_fields