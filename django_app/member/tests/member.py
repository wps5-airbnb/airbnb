"""
여기있는 테스트는 기능테스트이므로 나중에 기능 테스트로 통합할 예정
"""
from django.test import TestCase, Client
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
        SignUp에 필드가 정상적으로 들어 갔는지 확인하는 부분
        """
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["email"], test_user["email"])
        self.assertEqual(result["first_name"], test_user["first_name"])
        self.assertEqual(result["last_name"], test_user["last_name"])
        self.assertEqual(result["birthday"], test_user["birthday"])

        """
        MyUser객체가 잘 만들어 졌는지 확인하는 부분
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
