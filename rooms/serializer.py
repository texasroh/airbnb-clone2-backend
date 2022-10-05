from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1  # show relationship
