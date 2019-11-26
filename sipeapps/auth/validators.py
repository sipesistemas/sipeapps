from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeLoginValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+$'
    message = _(
        'Digite um login válido. Este valor pode conter apenas letras, '
        'número e @/./+/-/_ caracteres.'
    )
    flags = 0
