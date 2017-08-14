from django.views.generic import CreateView
from rest_framework import generics, permissions, filters

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

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user', 'house')

    def perform_create(self, serializer):
        serializer.save()


class ReservationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    ]
