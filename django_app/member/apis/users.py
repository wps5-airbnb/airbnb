from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import ObjectIsRequestUser
from ..models import MyUser
from ..serializers import UserSerializer, UserCreateSerializer

__all__ = [
    'UserCreateListView',
    'UserRetrieveUpdateDestroyView',
]


class UserCreateListView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        elif self.request.method == 'GET':
            return UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save(email=self.request.POST['email'])
        if serializer._context["request"].FILES is not None:
            img_profile_gen = serializer._context["request"].FILES.values()

            for img_profile in img_profile_gen:
                instance.img_profile = img_profile
                instance.save()
                break


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

