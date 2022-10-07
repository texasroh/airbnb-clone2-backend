from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
        # depth = 1  # show relationship

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        return room.owner == request.user


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    # reviews = ReviewSerializer(read_only=True, many=True)
    photos = PhotoSerializer(many=True, read_only=True)
    is_liked = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context.get("request")
        return Wishlist.objects.filter(user=request.user, rooms=room).exists()
