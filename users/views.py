from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions


class Me(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pass

    def put(self, request):
        pass
