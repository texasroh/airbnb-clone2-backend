from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = models.Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        print(request.data)
        return Response({"created": True})


@api_view()
def category(request, pk):
    category = models.Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)
