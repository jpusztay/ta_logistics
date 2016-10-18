from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json


def validate_optional_field_json(value):
    try:
        json.loads(value)
    except ValueError:
        raise ValidationError(
            _('%(value)s is not a valid JSON String, cannot commit to DB'),
            params={'value': value},
        )