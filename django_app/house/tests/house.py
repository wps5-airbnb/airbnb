"""
이곳의 있는 내용은 기능테스트의 내용입니다(This is Not Unit test)
"""
import filecmp

from django.test import TestCase
from django.test.client import encode_multipart
from rest_framework.test import APIClient

from house.models import House, Amenities
from member.models import MyUser


class HouseAPITest(TestCase):
    def setUp(self):
        # test User 생성
        self.user = MyUser.objects.create_user(
            username='test_user10@gmail.com',
            email='test_user10@gmail.com',
            password='asd1234567'
        )

        # User를 로그인 시키는 부분
        test_user = {
            'email': 'test_user10@gmail.com',
            'password': 'asd1234567'
        }
        self.client = APIClient()
        response = self.client.post(
            '/apis/user/login/',
            test_user,
        )

        login_result = response.json()
        token = login_result['token']

        # 로그인시 받아진 토큰을 헤더에 넣는 부분
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + token

        # test 용 dummy house 만들기
        self.dummy_house1 = House.objects.create(
            host=self.user,
            title='첫번째 숙소',
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

        self.dummy_house2 = House.objects.create(
            host=self.user,
            title='두번째 숙소',
            price_per_day=30000,
            extra_people_fee=10000,
            cleaning_fee=5000,
            weekly_discount=12,
            accommodates=3,
            bathrooms=1,
            bedrooms=1,
            beds=1,
            latitude=12.1234,
            longitude=127.1234,
        )

        # 테스트용 데이터베이스에 Amenities 셋팅
        lists = ['Pets_allowed', 'Elevator', 'Gym', 'Indoor_fireplace', 'Internet',
                 'Doorman', 'Kitchen', 'Pool', 'Smoking_allowed', 'Wheelchair_accessible',
                 'Wireless_Internet', 'Free_parking', 'Breakfast', 'Dryer', 'Cable_TV', 'Hangers',
                 'Washer', 'Shampoo', 'Essentials', 'Heating', 'TV', 'Air_conditioning', ]

        for item in lists:
            Amenities.objects.create(name=item)

    def test_house_list(self):
        """
        House list 기능을 테스트 합니다.
        :return: N/A
        """
        response = self.client.get('/apis/house/')
        result = response.json()

        self.assertEqual(response.status_code, 200)

        for house in result:
            house_in_db = House.objects.get(pk=house['pk'])
            self.assertEqual(house['title'], house_in_db.title)
            self.assertEqual(house['price_per_day'], house_in_db.price_per_day)
            self.assertEqual(house['extra_people_fee'], house_in_db.extra_people_fee)
            self.assertEqual(house['cleaning_fee'], house_in_db.cleaning_fee)
            self.assertEqual(house['weekly_discount'], house_in_db.weekly_discount)
            self.assertEqual(house['accommodates'], house_in_db.accommodates)
            self.assertEqual(house['bathrooms'], house_in_db.bathrooms)
            self.assertEqual(house['bedrooms'], house_in_db.bedrooms)
            self.assertEqual(house['beds'], house_in_db.beds)
            self.assertEqual(house['latitude'], house_in_db.latitude)
            self.assertEqual(house['longitude'], house_in_db.longitude)

    def test_house_create(self):
        """
        House Create(Hosting) 기능을 테스트 합니다.
        :return: N/A
        """
        request_image1 = open('../.media/user/jeakyung.jpg', 'rb')  # image를 binary형식으로 open 후 저장
        request_image2 = open('../.media/user/jeakyung.jpg', 'rb')  # image를 binary형식으로 open 후 저장

        house_content = {
            'title': '이 숙소의 제목입니다.',
            'price_per_day': 40000,
            'extra_people_fee': 20000,
            'cleaning_fee': 8000,
            'weekly_discount': 10,
            'accommodates': 4,
            'bathrooms': 2,
            'bedrooms': 2,
            'beds': 2,
            'latitude': 12.1234,
            'longitude': 127.1234,
            'image1': request_image1,
            'image2': request_image2,
        }

        encoded_content = encode_multipart('BoUnDaRyStRiNg', house_content)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = self.client.post(
            '/apis/house/',
            encoded_content,
            content_type=content_type,
        )

        result = response.json()

        request_image1.close()
        request_image2.close()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(result['host']['username'], self.user.username)

        #  보냈던 요청의 내용과 Response의 내용이 일치하는지 검증하는 부분
        self.assertEqual(result['title'], house_content['title'])
        self.assertEqual(result['price_per_day'], house_content['price_per_day'])
        self.assertEqual(result['extra_people_fee'], house_content['extra_people_fee'])
        self.assertEqual(result['cleaning_fee'], house_content['cleaning_fee'])
        self.assertEqual(result['weekly_discount'], house_content['weekly_discount'])
        self.assertEqual(result['accommodates'], house_content['accommodates'])
        self.assertEqual(result['bathrooms'], house_content['bathrooms'])
        self.assertEqual(result['bedrooms'], house_content['bedrooms'])
        self.assertEqual(result['beds'], house_content['beds'])
        self.assertEqual(result['latitude'], house_content['latitude'])
        self.assertEqual(result['longitude'], house_content['longitude'])

        #  House객체가 원래 의도대로 잘 만들어 졌는지 검증하는 부분
        house = House.objects.get(pk=result['pk'])

        self.assertEqual(result['title'], house.title)
        self.assertEqual(result['price_per_day'], house.price_per_day)
        self.assertEqual(result['extra_people_fee'], house.extra_people_fee)
        self.assertEqual(result['cleaning_fee'], house.cleaning_fee)
        self.assertEqual(result['weekly_discount'], house.weekly_discount)
        self.assertEqual(result['accommodates'], house.accommodates)
        self.assertEqual(result['bathrooms'], house.bathrooms)
        self.assertEqual(result['bedrooms'], house.bedrooms)
        self.assertEqual(result['beds'], house.beds)
        self.assertEqual(result['latitude'], house.latitude)
        self.assertEqual(result['longitude'], house.longitude)

        #  House 이미지 업로드가 정상적으로 되었는지 검증하는 부분(같은 사진을 두장 업로드했고, 이 두장이 기존에 보냈던 두장이 맞는지 확인)
        request_image_url = '../.media/user/jeakyung.jpg'
        for image in house.image.all():
            self.assertTrue(filecmp.cmp(request_image_url, '../.media/{}'.format(image.image)))

    def test_house_update(self):
        """
        시나리오
            image -> 기존의 사진은 그대로 두고 다른 사진 2장을 추가하는 상황
            숙소의 이름 변경
            숙소에 대한 소개 및 내용 추가
            숙소 편의시설(Amenities) 추가
        :return:
        """

        request_image1 = open('../.media/HouseImage/suji2.jpg', 'rb')  # image를 binary형식으로 open 후 저장
        request_image2 = open('../.media/HouseImage/suji3.jpg', 'rb')  # image를 binary형식으로 open 후 저장

        house_content = {
            'title': '변경된 숙소의 제목',
            'price_per_day': 80000,
            'extra_people_fee': 30000,
            'cleaning_fee': 10000,
            'weekly_discount': 7,
            'accommodates': 3,
            'bathrooms': 1,
            'bedrooms': 1,
            'beds': 1,
            'latitude': 12.1234,
            'longitude': 127.1234,
            'image1': request_image1,
            'image2': request_image2,
            'address': '서울시 강남구 신사역 근처',
            'introduce': '서울시내 한복판에 있어서 교통이 좋고, 접근성이 좋습니다.',
            'space_info': '숙소 내 모든 시설을 제한없이 이용할 수 있습니다.',
            'guest_access': '내부에 애완동물과 같이 올 수 있습니다.',
            'amenities': 'TV, Internet, Pool'
        }

        encoded_content = encode_multipart('BoUnDaRyStRiNg', house_content)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'

        response = self.client.patch(
            '/apis/house/1/',
            encoded_content,
            content_type=content_type,
        )

        request_image1.close()
        request_image2.close()

        result = response.json()

        self.assertEqual(response.status_code, 200)

        # Response Check
        self.assertEqual(result['host']['pk'], self.user.pk)
        self.assertEqual(result['title'], house_content['title'])
        self.assertEqual(result['price_per_day'], house_content['price_per_day'])
        self.assertEqual(result['extra_people_fee'], house_content['extra_people_fee'])
        self.assertEqual(result['cleaning_fee'], house_content['cleaning_fee'])
        self.assertEqual(result['weekly_discount'], house_content['weekly_discount'])
        self.assertEqual(result['accommodates'], house_content['accommodates'])
        self.assertEqual(result['bathrooms'], house_content['bathrooms'])
        self.assertEqual(result['bedrooms'], house_content['bedrooms'])
        self.assertEqual(result['beds'], house_content['beds'])
        self.assertEqual(result['latitude'], house_content['latitude'])
        self.assertEqual(result['longitude'], house_content['longitude'])
        self.assertEqual(result['address'], house_content['address'])
        self.assertEqual(result['introduce'], house_content['introduce'])
        self.assertEqual(result['space_info'], house_content['space_info'])
        self.assertEqual(result['guest_access'], house_content['guest_access'])

        #  House객체가 원래 의도대로 잘 변경되었는지 검증하는 부분
        house = House.objects.get(pk=result['pk'])

        self.assertEqual(result['title'], house.title)
        self.assertEqual(result['price_per_day'], house.price_per_day)
        self.assertEqual(result['extra_people_fee'], house.extra_people_fee)
        self.assertEqual(result['cleaning_fee'], house.cleaning_fee)
        self.assertEqual(result['weekly_discount'], house.weekly_discount)
        self.assertEqual(result['accommodates'], house.accommodates)
        self.assertEqual(result['bathrooms'], house.bathrooms)
        self.assertEqual(result['bedrooms'], house.bedrooms)
        self.assertEqual(result['beds'], house.beds)
        self.assertEqual(result['latitude'], house.latitude)
        self.assertEqual(result['longitude'], house.longitude)
        self.assertEqual(result['address'], house.address)
        self.assertEqual(result['introduce'], house.introduce)
        self.assertEqual(result['space_info'], house.space_info)
        self.assertEqual(result['guest_access'], house.guest_access)

        # Amenities가 정상적으로 들어갔는지 검증하는 부분
        request_amenities = [i.strip() for i in house_content['amenities'].split(',')].sort()
        created_amenities = [i.name for i in house.amenities.all()].sort()

        self.assertEqual(request_amenities, created_amenities)

        # Image가 정상적으로 추가되었는지 검증하는 부분
        request_image_url1 = '../.media/HouseImage/suji2.jpg'
        request_image_url2 = '../.media/HouseImage/suji3.jpg'
        created_images = ['../.media/{}'.format(url.image) for url in house.image.all()]

        self.assertTrue(filecmp.cmp(request_image_url1, created_images[0]))
        self.assertTrue(filecmp.cmp(request_image_url2, created_images[1]))
