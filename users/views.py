import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from .serializers import PrivateUserSerializer
from .models import User


class Me(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        serializer = PrivateUserSerializer(
            request.user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError("Need password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise exceptions.ValidationError(e)
        serializer = PrivateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.set_password(password)
        user.save()
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise exceptions.ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "wrong password"})

        login(request, user)
        return Response({"ok": "Welcome!"})


class LogOut(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "wrong password"})

        token = jwt.encode({"pk": user.pk}, key=settings.SECRET_KEY, algorithm="HS256")
        return Response({"token": token})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id={settings.GITHUB_CLIENT_ID}&client_secret={settings.GITHUB_CLIENT_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            ).json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            ).json()
            email = user_emails[0]["email"]
            for user_email in user_emails:
                if user_email["primary"]:
                    email = user_email["email"]

            print(user_data)
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=email,
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "authorization_code",
                        "client_id": settings.KAKAO_CLIENT_ID,
                        "redirect_uri": "http://localhost:3000/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded;charset_utf-8",
                },
            ).json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("id"),
                    email=kakao_account.get("email"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
