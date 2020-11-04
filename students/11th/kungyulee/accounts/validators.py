import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_number(number):
    number_regex = r'^\d{3}-\d{4}-\d{4}$'
    regex        = re.compile(number_regex)

    if not regex.match(number):
        raise ValidationError(
            _('%(number)s is not a valid number'),
            params = {'number' : number},
        )

def validate_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*\d)[a-z\d]{8,}$'
    regex          = re.compile(password_regex)

    if not regex.match(password):
        raise ValidationError(
            _('%(password)s is not a valid number'),
            params = {'password' : password},
        )
