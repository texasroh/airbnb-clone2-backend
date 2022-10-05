from rest_framework.serializers import ModelSerializer
from . import models


class PerkSerializer(ModelSerializer):
    class Meta:
        model = models.Perk
        fields = "__all__"
