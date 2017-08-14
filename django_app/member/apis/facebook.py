import requests
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer

__all__ = [
    'FacebookLoginView',
]

User = get_user_model()


class FacebookLoginView(APIView):
    FACEBOOK_APP_ID = '109545549725622'
    FACEBOOK_SECRET_CODE = '7849ce8eda45d7d55665a880c1d8d433'

    APP_ACCESS_TOKEN = '{}|{}'.format(
        FACEBOOK_APP_ID,
        FACEBOOK_SECRET_CODE,
    )

    def post(self, request):
        token = request.data.get('token')
        if not token:
            raise APIException('token require')

        self.debug_token(token)
        user_info = self.get_user_info(token=token)
        username = '{id}@crusia.xyz'.format(id=user_info['id'])
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_facebook_user(user_info=user_info, username=username)

        token, token_created = Token.objects.get_or_create(user=user)

        # 관련정보를 한번에 리턴
        ret = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(ret)


    def debug_token(self, token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': self.APP_ACCESS_TOKEN
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()

        if 'error' in result['data']:
            raise APIException('token invalid')
        return result

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/me'
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result
