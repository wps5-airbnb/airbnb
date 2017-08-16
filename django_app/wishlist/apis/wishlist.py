from rest_framework import authentication, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from house.models import House
from house.serializers.house import HouseSerializer
from ..models import Wishlist

__all__ = [
    'WishlistView',
]


class WishlistView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request):
        user = request.user
        house_pk = int(request.query_params['house'])
        house = House.objects.get(pk=house_pk)
        instance, created = Wishlist.objects.get_or_create(
            liker=user,
            house=house,
        )

        if not created:
            instance.delete()
            return Response(
                '{}유저가 pk={}인 하우스의 좋아요를 취소하였습니다.'.format(user.username, house.pk),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                '{}유저가 pk={}인 하우스를 좋아합니다.'.format(user.username, house.pk),
                status=status.HTTP_201_CREATED,
            )

    def get(self, request):
        user = request.user
        like_houses = user.get_wishlist.all()
        serializer = HouseSerializer(like_houses, many=True)
        return Response(serializer.data)
