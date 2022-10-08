from rest_framework.serializers import ModelSerializer
from . import models


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ("name", "avatar", "username")


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "id",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
