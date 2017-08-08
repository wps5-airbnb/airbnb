from rest_framework import generics, permissions

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

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        house_content = self.request.data.get('house')
        if house_content:
            instance.user = Reservations.objects.create(
                reservation=instance,
                user=instance.user,
                content=house_content,
            )
            instance.save()


class ReservationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,
    ]
