from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    """Register a user already active, without email verification needed"""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password1"],
        )
        return user

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data


class UserSerializer(serializers.ModelSerializer):
    """Register user with extra fields and set as inactive at first"""

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "input_company_name",
            "cellphone",
        )

    def create(self, validated_data):
        user_data = {
            "email": validated_data["email"],
            "password": validated_data["password1"],
            "is_active": False,
        }
        # Dont add extra fields if they are not present
        if "first_name" in validated_data:
            user_data["first_name"] = validated_data["first_name"]
        if "last_name" in validated_data:
            user_data["last_name"] = validated_data["last_name"]
        if "input_company_name" in validated_data:
            user_data["input_company_name"] = validated_data["input_company_name"]
        if "cellphone" in validated_data:
            user_data["cellphone"] = validated_data["cellphone"]

        user = User.objects.create_user(**user_data)

        return user

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match.")
        return data
