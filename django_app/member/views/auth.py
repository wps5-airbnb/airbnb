from django.contrib.auth import \
    login as django_login, \
    logout as django_logout, get_user_model
from django.shortcuts import redirect, render

from ..forms.login import LoginForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
)


def login(request):
    # POST요청이 왔을 경우
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('index.html')
    else:
        if request.user.is_authenticated:
            return redirect('index.html')
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    pass


def signup(requset):
    pass


def facebook_login(request):
    pass
