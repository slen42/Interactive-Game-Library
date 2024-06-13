from typing import Any
from password_validator import PasswordValidator
from wtforms import ValidationError

class ValidPassword:
    def __init__(self, message=None) -> None:
        if not message:
            message = "Your password must be at least 7 characters."
        self.message = message

    def __call__(self, form, field) -> Any:
        schema = PasswordValidator()
        schema.min(7).has().digits()

        if not schema.validate(field.data):
            raise ValidationError(self.message)