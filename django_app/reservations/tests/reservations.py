from django.test import TestCase

from house.models import House
from member.models import MyUser


class ReservationsAPITest(TestCase):
    def setUp(self):
        # Host User 생성
        self.host_user = MyUser.objects.create_user(
            username='test_user10@gmail.com',
            email='test_user10@gmail.com',
            password='asd1234567'
        )

        # Guest User 생성
        self.guest_user = MyUser.objects.create_user(
            username='test_user11@gmail.com',
            email='test_user11@gmail.com',
            password='asd1234567'
        )

        # Host User 숙소 등록
        self.house = House.objects.create(
            host=self.host_user,
            title='예약이 가능한 숙소 입니다.',
            introduce='어서오세요',
            price_per_day=40000,
            extra_people_fee=20000,
            cleaning_fee=8000,
            weekly_discount=10,
            accommodates=4,
            bathrooms=1,
            bedrooms=1,
            beds=1,
            latitude=12.1234,
            longitude=127.1234,
        )