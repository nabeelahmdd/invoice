import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class NumberValidator(object):
    """
        validate password contain at least one digits.
    """
    def validate(self, password, user=None):
        if not re.findall('\d{1,}', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-8."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-8."
        )


class SymbolValidator(object):
    """
        validate password contain at least one special character.
    """
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]{1,}', password):
            raise ValidationError(
                _("The password must contain at least 1 special character: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )