import typing
import strawberry
from strawberry import auto
from strawberry.types import Info
from django.conf import settings
from django.core.paginator import Paginator
from . import models
from users.types import UserType
from reviews.types import ReviewType
from wishlists.models import Wishlist


@strawberry.django.type(models.Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: UserType

    @strawberry.field
    def reviews(self, page: typing.Optional[int] = 1) -> typing.List[ReviewType]:
        page_size = settings.PAGE_SIZE
        # start = (page - 1) * page_size
        # end = start + page_size
        paginator = Paginator(self.reviews.all(), page_size, orphans=2)
        return paginator.get_page(page)

    @strawberry.field
    def rating(self) -> str:
        return self.rating()

    @strawberry.field
    def is_owner(self, info: Info) -> bool:
        return info.context.request.user == self.owner

    @strawberry.field
    def is_liked(self, info: Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user, rooms=self
        ).exists()
