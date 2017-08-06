from django.db import models
from django.utils import timezone
from rest_framework import generics, permissions

from utils.permissions import IsHouseOwner
from .paginator import ResultsSetPagination
from ..models import House, Amenities
from ..serializers.house import HouseSerializer

__all__ = [
    'HouseCreateListView',
    'HouseRetrieveUpdateDestroyView',
    'HouseCreateListViewWithPage',
]


class HouseCreateListView(generics.ListCreateAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        """
        다중 이미지 저장을 위해서 구현(그냥 모든 파일을 이미지로 만듬, 여기서 파일 입출력은 이미지 형식에 국한되어 있다고 가정.
        :param serializer: Post 요청시 받는 DATA가 있는 serializer
        :return: None, 이미지의 변수이름 상관없이 모든 파일 다 긁어 옴
        """
        instance = serializer.save(host=self.request._user)
        images_dict = serializer._context["request"].FILES
        images = images_dict.values()
        if images:
            for image in images:
                instance.image.create(
                    house=instance,
                    image=image,
                )
        built_in_amenities = [i.name for i in Amenities.objects.all()]
        amenities_list = [i.strip() for i in serializer._context["request"].POST["amenities"].split(',')]
        if len(amenities_list) - 1:
            for name in amenities_list:
                if name in built_in_amenities:
                    instance.amenities.add(Amenities.objects.get(name=name))
                    instance.save()
                else:
                    raise ValueError("Amenities {}의 이름이 올바르지 않습니다.(스펠링, 대소문자, 쉼표구분 체크하세요)".format(name))


class HouseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsHouseOwner,
    ]
    """
    이미지 update 관련 이슈
    """

    # 이미지 삭제 요청 > 어떻게 받을 것인지
    # 이미지 추가 > 요건 쉬움
    # 이미지 바꾸기 > 요건 어떻게?

    def perform_update(self, serializer):
        """
        일단 PATCH단계에서 이미지를 가져오면 그냥 중복여부 상관없이 무조건 새로 추가해줌
        """

        instance = House.objects.get(pk=self.kwargs["pk"])

        built_in_amenities = [i.name for i in Amenities.objects.all()]
        if serializer._context["request"].POST.get("amenities") is not None and serializer._context["request"].POST.get("amenities") is not '':
            amenities_list = [i.strip() for i in serializer._context["request"].POST["amenities"].split(',')]
            if len(amenities_list) - 1:
                instance.amenities.clear()
                for name in amenities_list:
                    if name in built_in_amenities:
                        instance.amenities.add(Amenities.objects.get(name=name))
                        instance.save()
                    else:
                        raise ValueError("Amenities {}의 이름이 올바르지 않습니다.(스펠링, 대소문자, 쉼표구분 체크하세요)".format(name))

        # House 이미지 삭제요청이 들어온 경우
        if serializer._context["request"].POST.get("image_crusher") is not None and serializer._context["request"].POST.get("image_crusher") is not '':
            death_note = [i.strip() for i in serializer._context["request"].POST["image_crusher"].split(',')]
            for order_num in death_note:
                try:
                    instance.image.get(_order=order_num)
                except models.ObjectDoesNotExist:
                    pass
                else:
                    if instance.image.get(_order=order_num) is not None:
                        instance.image.get(_order=order_num).delete()
                        instance.save()

        # 이미지 신규 등록부분
        if serializer._context["request"].FILES is not None:
            images_dict = serializer._context["request"].FILES
            images = images_dict.values()
            for image in images:
                instance.image.create(
                    house=instance,
                    image=image,
                )

        # House에 해당하는 이미지의 순서를 재기록
        for index, image in enumerate(instance.image.all()):
            image._order = index
            image.save()

        # modified_date update
        instance.modified_date = timezone.now()
        instance.save()

        serializer.save()


# lists = ['Pets_allowed', 'Elevator', 'Gym', 'Indoor_fireplace', 'Internet',
#          'Doorman', 'Kitchen', 'Pool', 'Smoking_allowed', 'Wheelchair_accessible',
#          'Wireless_Internet', 'Free_parking', 'Breakfast', 'Dryer', 'Cable_TV', 'Hangers',
#          'Washer', 'Shampoo', 'Essentials', 'Heating', 'TV', 'Air_conditioning', ]


class HouseCreateListViewWithPage(HouseCreateListView):
    pagination_class = ResultsSetPagination
