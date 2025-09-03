from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password: serializers.CharField = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2: serializers.CharField = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "password", "password2")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        user = CustomUser.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username: serializers.CharField = serializers.CharField(required=True)
    password: serializers.CharField = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Неверные данные для входа")
        attrs["user"] = user
        return attrs
