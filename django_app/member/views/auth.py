from django.contrib.auth import get_user_model

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
)


def login(request):
    pass


def logout(request):
    pass


def signup(requset):
    pass


def facebook_login(request):
    pass
