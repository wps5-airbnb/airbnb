from pprint import pprint

from datetime import timedelta, datetime
from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework.test import APIClient

from house.models import House
from member.models import MyUser
from reservations.models import Reservations


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

    def test_make_reservations(self):
        # guest user login
        guest_user = {
            'email': 'test_user11@gmail.com',
            'password': 'asd1234567'
        }
        client = APIClient()
        login_response = client.post(
            '/apis/user/login/',
            guest_user,
        )
        login_result = login_response.json()
        token = login_result['token']
        client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + token

        # guest user make reservations
        reservations_contents = {
            'checkin_date': '2017-08-25',
            'checkout_date': '2017-08-27',
            'message_to_host': '잘 부탁드립니다.',
            'adults': 2,
            'children': 0,
            'infants': 0,
        }
        encoded_content = encode_multipart('BoUnDaRyStRiNg', reservations_contents)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = client.post(
            '/apis/reservations/?house=1',
            encoded_content,
            content_type=content_type,
        )

        result = response.json()
        pprint(result)

        # HTTP status code 확인
        self.assertEqual(response.status_code, 201)

        # 생성된 reservations객체 확인
        reservation = Reservations.objects.get(guest=self.guest_user)

        self.assertEqual(reservations_contents['checkin_date'], reservation.checkin_date.strftime('%Y-%m-%d'))
        self.assertEqual(reservations_contents['checkout_date'], reservation.checkout_date.strftime('%Y-%m-%d'))
        self.assertEqual(reservations_contents['message_to_host'], reservation.message_to_host)
        self.assertEqual(reservations_contents['adults'], reservation.adults)
        self.assertEqual(reservations_contents['children'], reservation.children)
        self.assertEqual(reservations_contents['infants'], reservation.infants)

        # House disable_days에 정상적으로 추가되었는지 검증하는 부분
        house = House.objects.get(pk=1)
        request_reserved_dates = [datetime.strptime(reservations_contents['checkin_date'], '%Y-%m-%d').date() + timedelta(n) for n in range((datetime.strptime(reservations_contents['checkout_date'], '%Y-%m-%d') - datetime.strptime(reservations_contents['checkin_date'], '%Y-%m-%d')).days)]
        created_disable_days = [i.date for i in house.disable_days.all()]

        for day in request_reserved_dates:
            self.assertTrue(day in created_disable_days)





