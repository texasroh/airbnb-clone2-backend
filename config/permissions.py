from rest_framework.authentication import BaseAuthentication


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)
