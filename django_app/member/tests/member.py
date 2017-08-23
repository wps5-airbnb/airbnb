"""
여기있는 테스트는 기능테스트이므로 나중에 기능 테스트로 통합할 예정(This is Not Unit test)
"""
import filecmp
from django.test import TestCase, Client
from django.test.client import encode_multipart
from rest_framework.authtoken.models import Token

from member.models import MyUser


class UserAPITest(TestCase):
    """
    MyUser 모델을 테스트 합니다. Am
    """

    # Up은 대문자 U
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='test_user10@gmail.com',
            email='test_user10@gmail.com',
            password='asd1234567'
        )

    # 반드시 test로 시작을 해야 이 장고가 알아 먹는다
    def test_signup(self):
        """
        일반 장고유저, 회원가입이 요청 테스트
        :return: None
        """
        test_user = {
            'email': 'test_user12@gmail.com',
            'password1': 'asd1234567',
            'password2': 'asd1234567',
            'first_name': 'Linda',
            'last_name': 'Sorry',
            'birthday': '1980-09-25'
        }

        client = Client()
        response = client.post(
            '/apis/user/',
            test_user,
        )
        result = response.json()

        """
        SignUp 요청의 내용과 Response의 내용이 일치하는지 검증하는 부분
        """
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["email"], test_user["email"])
        self.assertEqual(result["first_name"], test_user["first_name"])
        self.assertEqual(result["last_name"], test_user["last_name"])
        self.assertEqual(result["birthday"], test_user["birthday"])

        """
        MyUser객체가 잘 만들어 졌는지 검증하는 부분
        """
        user = MyUser.objects.get(username=test_user["email"])
        self.assertEqual(test_user["email"], user.email)
        self.assertEqual(test_user["first_name"], user.first_name)
        self.assertEqual(test_user["last_name"], user.last_name)
        self.assertEqual(test_user["birthday"], user.birthday.strftime('%Y-%m-%d'))

    def test_login(self):
        """
        이메일 유저가 정상적으로 로그인이 되는지 확인하는 부분
        :return:
        """
        test_user = {
            'email': 'test_user10@gmail.com',
            'password': 'asd1234567'
        }
        client = Client()
        response = client.post(
            '/apis/user/login/',
            test_user,
        )
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['token'], Token.objects.get(user_id=self.user.pk).key)

    def test_user_update(self):
        # User를 로그인 시키는 부분
        test_user = {
            'email': 'test_user10@gmail.com',
            'password': 'asd1234567'
        }
        client = Client()
        response = client.post(
            '/apis/user/login/',
            test_user,
        )
        login_result = response.json()
        token = login_result['token']

        # 로그인시 받아진 토큰을 헤더에 넣는 부분
        client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + token

        # User Update 요청 부분
        user_pk = MyUser.objects.get(username='test_user10@gmail.com').pk

        img = open('../.media/user/jeakyung.jpg', 'rb')  # image를 binary형식으로 open 후 저장

        request_contents = {
            'first_name': 'NotLinda',
            'last_name': 'NoSorry',
            'birthday': '1990-01-30',
            'gender': 'MALE',
            'phone_num': '010-1234-5678',
            "preference_language": 'Korean',
            "preference_currency": 'Won',
            "living_site": 'Seoul',
            "introduce": 'Hi, Nice to meet you',
            "img_profile": img,
        }

        # Patch 요청은 encoding을 해야 함
        encoded_content = encode_multipart('BoUnDaRyStRiNg', request_contents)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = client.patch(
            '/apis/user/{}/'.format(user_pk),
            encoded_content,
            content_type=content_type,
        )
        img.close()

        result = response.json()

        # 요청 상태 확인
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(result['first_name'], 'Linda')
        self.assertNotEqual(result['last_name'], 'Sorry')
        self.assertNotEqual(result['birthday'], '1980-09-25')
        self.assertNotEqual(result['gender'], 'OTHER')
        self.assertNotEqual(result['phone_num'], 'null')
        self.assertNotEqual(result['preference_language'], 'null')
        self.assertNotEqual(result['preference_currency'], 'null')
        self.assertNotEqual(result['living_site'], 'null')
        self.assertNotEqual(result['introduce'], 'null')
        self.assertNotEqual(result['img_profile'], 'null')

        self.assertEqual(result['first_name'], 'NotLinda')
        self.assertEqual(result['last_name'], 'NoSorry')
        self.assertEqual(result['birthday'], '1990-01-30')
        self.assertEqual(result['gender'], 'MALE')
        self.assertEqual(result['phone_num'], '010-1234-5678')
        self.assertEqual(result['preference_language'], 'Korean')
        self.assertEqual(result['preference_currency'], 'Won')
        self.assertEqual(result['living_site'], 'Seoul')
        self.assertEqual(result['introduce'], 'Hi, Nice to meet you')

        # img_profile 검사

        origin_img = '../.media/user/jeakyung.jpg'
        saved_img = MyUser.objects.get(pk=user_pk).img_profile
        self.assertTrue(filecmp.cmp(origin_img, '../.media/{}'.format(saved_img)))

    def test_logout(self):
        """
        이메일 유저 및 페이스북 유저가 로그아웃이 되는지 확인하는 부분
        1. 로그인을 먼저 시킨후
        2. 그다음 바로 로그아웃
        :return:
        """

        # User를 로그인 시키는 부분
        test_user = {
            'email': 'test_user10@gmail.com',
            'password': 'asd1234567'
        }
        client = Client()
        response = client.post(
            '/apis/user/login/',
            test_user,
        )
        login_result = response.json()
        token = login_result['token']

        # 로그인시 받아진 토큰을 헤더에 넣는 부분
        client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + token

        # 다시 로그아웃 요청
        response = client.get(
            '/apis/user/logout/',
        )
        logout_result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(logout_result, 'Logout Completed')

    def test_user_delete(self):
        # User를 로그인 시키는 부분
        test_user = {
            'email': 'test_user10@gmail.com',
            'password': 'asd1234567'
        }
        client = Client()

        response = client.post(
            '/apis/user/login/',
            test_user,
        )
        login_result = response.json()
        token = login_result['token']

        # 로그인시 받아진 토큰을 헤더에 넣는 부분
        client = Client()
        client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + token

        # User 삭제 요청을 하는 부분
        user_pk = MyUser.objects.get(username='test_user10@gmail.com').pk

        response = client.delete(
            '/apis/user/{}/'.format(user_pk),
        )

        self.assertEqual(response.status_code, 204)
