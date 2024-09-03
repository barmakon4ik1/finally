from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from housing.variables import *


""" 
Модель класса пользователя

Администратор - суперпользователь, имеет доступ к базе данных и всем правам
Владелец (Owner) - арендодатель, может создавать, изменять объявления
Юзер - арендатор, может просматривать объявления, резервировать объекты и давать отзывы и резюмировать

Поля:
○ username (Строковое поле, уникальное, обязательно к заполнению)
○ first_name (строковое поле, обязательно к заполнению)
○ last_name (строковое поле, обязательно к заполнению)
○ email (поле email, уникальное, обязательное к заполнению)
○ phone (строковое поле, не обязательное)
○ is_staff (административное логическое поле, по умолчанию False)
○ is_active (логическое поле, по умолчанию True)
○ date_joined (Поле даты и времени, заполняется автоматически при создании)
○ last_login (Поле даты и времени, заполняется при входе в систему)
○ updated_at (Поле даты и времени, заполняется автоматически при всех обновлениях)
○ deleted_at (Поле даты и времени, заполняется только если поле deleted переходит в состояние True)
○ deleted (Логическое поле, по умолчанию - True)
○ position - тип пользователя
"""


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(
        _("first name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        name="registered", auto_now_add=True
    )
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    position = models.CharField(
        max_length=15,
        choices=UserType.choices,
        default=UserType.U
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "position",
    ]

    objects = UserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


"""
Модели для объекта недвижимости.

Включают в себя модели Address и Housing
***
Адрес состоит из полей:
country - название страны
city - населенный пункт
street - улица
house_number - номер дома (может быть с буквой и т.п. - до 6 символов)
postal_code - почтовый индекс
***
Объект недвижимости Housing имеет поля:
name - наименование объекта
description - описание объекта
price - цена аренды объекта за сутки
rooms - число комнат
type - тип объекта
address - ссылка на класс адреса объекта
"""


class Address(models.Model):
    country = models.CharField(_('Country'), max_length=100)
    city = models.CharField(_('City'), max_length=100)
    street = models.CharField(_('Street'), max_length=100)
    house_number = models.CharField(_('Haus'), max_length=6)
    postal_code = models.CharField(_('Post'), max_length=100)

    def __str__(self):
        return f'{self.street}, {self.house_number}, {self.postal_code} {self.city}, {self.country}'

    class Meta:
        verbose_name_plural = _('Addresses')
        verbose_name = _('Address')


class Housing(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    description = models.TextField(_('Description'), )
    price = models.DecimalField(
        _('Price'),
        max_digits=10,
        decimal_places=2
    )
    rooms = models.IntegerField(_('Rooms'), )
    type = models.CharField(
        _('Type'),
        max_length=20,
        choices=HousingType.choices,
        default=HousingType.H
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='housing',
    )
    owner = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='housing_owner')

    def __str__(self):
        return self.name


"""
Класс Advert - записи объявлений о сдачи в аренду объектов

поля:
    object_name - объект аренды
    created_at - дата создания объявления
    updated_at - дата изменения объявления
    deleted_at - дата удаления объявления
    is_visible - видимость объявления
    owner - владелец объявления
"""


class Advert(models.Model):
    object_name = models.OneToOneField(
        Housing,
        on_delete=models.SET_NULL,
        null=True,
        related_name='object_name')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    owner = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='adverts_owner'
    )

    def __str__(self):
        return str(self.object_name)

    class Meta:
        verbose_name_plural = _('Adverts')
        verbose_name = _('Advert')
        ordering = ['-created_at']