from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from .serializers import CategorySerializer


@api_view()
def categories(request):
    all_categories = models.Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response({"ok": True, "categories": serializer.data})
