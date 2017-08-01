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

# class UserRetrieveUpdateDestroyView(APIView):
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#     )
#     @staticmethod
#     def get_object(pk):
#         try:
#             return MyUser.objects.get(pk=pk)
#         except MyUser.DoesNotExist:
#             raise Response(status.HTTP_404_NOT_FOUND)
#
#     # retrieve
#     def get(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     # update
#     def put(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # partial update
#     def patch(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # destroy
#     def delete(self, request, pk):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser
    )

