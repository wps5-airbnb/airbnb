from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from house.models import House
from member.models import MyUser
from utils.permissions import ObjectIsRequestUser
from ..models import Reservations
from ..serializers import ReservationSerializer

__all__ = [
    'ReservationCreateListView',
    'ReservationRetrieveUpdateDestroyView'
]


class ReservationCreateListView(generics.ListCreateAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    # def get_queryset(self):
    #     return Reservations.objects.filter(house__reservation_user_set=self.kwargs['pk'])
    #
    # def list(self, request, *args, **kwargs):
    #     # pk에 해당하는 house 작성자가 request.user인지 확인하고 출력
    #     user = request.user
    #
    #     # house pk가 존재하는지..
    #     try:
    #         house = House.objects.get(pk=kwargs['pk'])
    #     except House.DoesNotExist as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     # 요청하는 유저가 host인지 확인
    #     try:
    #         host = user.host
    #     except ObjectDoesNotExist as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def create(self, request, *args, **kwargs):
    #     request.data['user'] = request.user.id
    #     serializer = ReservationSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     house = House.objects.get(pk=request.data['house_pk'])
    #     host = house.host
    #
    #     data = {
    #         'user': request.user,
    #         'host_house': house,
    #     }
    #
    #     if verify_duplicate(Reservations, data=data):
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     return Response(status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ReservationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    ]
