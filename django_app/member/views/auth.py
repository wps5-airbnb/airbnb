from pprint import pprint

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import \
    login as django_login, \
    logout as django_logout, get_user_model
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

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
            return redirect('index')
    else:
        if request.user.is_authenticated:
            return redirect('index')
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


def facebook_login(request):
    code = request.GET.get('code')
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    class GetAccessTakenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['data']['error']
            self.code = error_dict['code']
            self.message = error_dict['message']
            self.is_valid = error_dict['is_valid']
            self.scopes = error_dict['scopes']

    class DebugTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['data']['error']
            self.code = error_dict['code']
            self.message = error_dict['message']

    def add_message_and_redirect_referer():
        """
        페이스북 로그인 오류 메시지를 request에 추가하고, 이전 페이지로 redirect
        :return: redirect
        """
        # 유저용 메세지
        error_message_for_user = 'Facebook login error'
        # request에 에러메세지를 전달
        messages.error(request, error_message_for_user)
        # 이전페이지로 redirect
        return redirect(request.META['HTTP_REFERER'])

    def get_access_token(code):
        """
        code를 받아 액세스토큰 교환 URL에 요청, 이후 해당 액세스토큰을 반환
        오류 발생시 오류메시지를 리턴
        :param code:
        :return:
        """
        # 액세스토큰의 코드를 교환할 URL
        url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'

        # 이전에 요청했던 redirect_uri와 같은 값을 만들어 줌 (access_token을 요청할 때 필요함)
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
        )
        # 액세스토큰의 코드 교환
        # uri생성을 위한 params
        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        # 해당 URL에 get요청 후 결과 (json형식)를 파이썬 object로 변환 (result변수)
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        # 액세스토큰 코드교환 결과에 오류가 있을 경우
        # 해당 오류를 request에 message로 넘기고 이전페이지 (HTTP_REFERER)로 redirect
        elif 'error' in result:
            raise GetAccessTakenException(result)
        else:
            raise Exception('Unknown error')

    def debug_token(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': app_access_token
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        pprint(result)
        if 'error' in result['data']:
            raise DebugTokenException(result)
        else:
            return result

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'email',
                'picture.type(large)',
                'gender',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    # code키값이 존재하지 않으면 로그인을 더이상 진행하지 않음
    if not code:
        return add_message_and_redirect_referer()
    try:
        # 이 view에 GET parameter로 전달된 code를 사용해서 access_token을 받아옴
        # 성공시 access_token값을 가져옴
        # 실패시 GetAccessTokenException이 발생
        access_token = get_access_token(code)

        # 위에서 받아온 access_token을 이용해 debug_token을 요청
        # 성공시 토큰을 디버그한 결과 (user_id, scopes등..)이 리턴
        # 실패시 DebugTokenException이 발생
        debug_result = debug_token(access_token)

        # debug_result에 있는 user_id값을 이용해서 GraphAPI에 유저정보를 요청
        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)

        user = User.objects.get_or_create_facebook_user(user_info)
        # 해당 request에 유저를 로그인 시킴
        django_login(request, user)
        return redirect(request.META['HTTP_REFERER'])

    except GetAccessTakenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        # return add_message_and_redirect_referer()
