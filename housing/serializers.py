"""
Сериализаторы для моделей объекта и адреса
"""


from .models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re


class HousingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


"""
Сериализатор для класса пользователей

UserListSerializer - просмотр пользователей
RegisterUserSerializer - регистрация пользователей
"""


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'position',
            'email',
            'phone',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'position',
            'password',
            're_password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not re.match('^[a-zA-Z0-9_]*$', username):
            raise serializers.ValidationError({
                "username": "The username must be alphanumeric characters or have only _ symbol"
            })

        if not re.match('^[a-zA-Z]*$', first_name):
            raise serializers.ValidationError({
                "first_name": "The first name must contain only alphabet symbols"
            })

        if not re.match('^[a-zA-Z]*$', last_name):
            raise serializers.ValidationError({
                "last_name": "The last name must contain only alphabet symbols"
            })

        password = data.get("password")
        re_password = data.get("re_password")

        if password != re_password:
            raise serializers.ValidationError({"password": "Passwords don't match"})

        try:
            validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError({"password": err.messages})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


"""
Сериализатор для объявлений
"""


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = '__all__'
        