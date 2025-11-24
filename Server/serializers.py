from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from typing import Optional

User = get_user_model()

def calculate_age(dob: Optional[date]) -> Optional[int]:
    if not dob:
        return None
    today = date.today()
    years = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1
    return years

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        age = calculate_age(user.date_of_birth)

        token["email"] = user.email
        token["username"] = user.username
        token["age"] = age if age is not None else 0
        token["is_adult"] = bool(age is not None and age >= 18)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        age = calculate_age(user.date_of_birth)

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "date_of_birth": user.date_of_birth,
            "age": age if age is not None else 0,
            "is_adult": bool(age is not None and age >= 18),
            "is_staff": user.is_staff,
        }

        return data

class UserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    is_adult = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "date_of_birth",
            "age",
            "is_adult",
        )

    def get_age(self, obj: User):
        return calculate_age(obj.date_of_birth)

    def get_is_adult(self, obj: User):
        age = calculate_age(obj.date_of_birth)
        return bool(age is not None and age >= 18)
