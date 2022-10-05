from rest_framework.serializers import ModelSerializer
from . import models


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ("name", "avatar", "username")
