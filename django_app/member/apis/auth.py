from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import NewAuthTokenSerializer

__all__ = [
    'UserLogoutView',
    'obtain_auth_token',
]

User = get_user_model()


class ObtainAuthToken(APIView):
    """
    이게 로그인 기능 대용 : 로그인이 정상적으로 완료되면 토큰을 반환
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = NewAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return Response({
            'user_pk': user.pk,
            'user_name': user.email,
            'token': token.key
        })


obtain_auth_token = ObtainAuthToken.as_view()


class UserLogoutView(APIView):
    def get(self, request):
        token = Token.objects.get(key=request._auth)
        user = User.objects.get(pk=token.user_id)
        user.auth_token.delete()
        return Response('Logout Completed')
