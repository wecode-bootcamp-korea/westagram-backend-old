import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_email(value):
    email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    regex = re.compile(email_reg)

    if not regex.match(value):
        raise ValidationError(
            _('%(value)s is not a valid number'),
            params = {'value' : value},
        )

def validate_password(password):
    if len(password) <= 8:
        raise ValidationError("password is too short.")