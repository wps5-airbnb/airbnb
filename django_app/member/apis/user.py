from rest_framework import generics, permissions

from utils.permissions import ObjectIsRequestUser
from ..serializers import UserSerializer, UserCreationSerializer
from ..models import MyUser

__all__ = (
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )