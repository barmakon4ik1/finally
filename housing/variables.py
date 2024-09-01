"""
Значения для переменных выбора
"""
from enum import Enum
from django.utils.translation import gettext_lazy as _


class HousingType(Enum):
    H = _('Haus')
    A = _('Apartment')
    O = _('Office')
    S = _('Hall')
    L = _('Land plot')

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]


class UserType(Enum):
    U = _('User')
    A = _('Administrator')
    O = _('Owner')

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]

