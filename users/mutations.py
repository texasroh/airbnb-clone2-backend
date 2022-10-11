from strawberry.types import Info
from django.contrib.auth import authenticate, login, logout
from . import types


def log_in(login_info: types.LoginInfo, info: Info):
    username = login_info.username
    password = login_info.password
    user = authenticate(info.context.request, username=username, password=password)
    if not user:
        return False
    login(info.context.request, user)
    return True


def log_out(info: Info):
    logout(info.context.request)
    return True
