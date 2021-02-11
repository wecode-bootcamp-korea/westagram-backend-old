#-*- coding:utf-8 -*-
from django.test import Client, TestCase
from django.conf import settings
from django.http import JsonResponse

import json
import bcrypt
import jwt

from .models     import User
from .utils      import login_decorator

class SignUpTestCase(TestCase):
    def setUp(self):
        self.URL = '/user/signup'
        self.client = Client()
        self.GOOD_NAME          = 'myname'
        self.GOOD_EMAIL         = 'abcdefg@gmail.com'
        self.GOOD_PHONE_NUMBER  = '01012345678'
        self.GOOD_PASSWORD      = '12345678'

        self.DUMMY_NAME         = 'mr.dummy'
        self.DUMMY_EMAIL        = 'dummy@email.com'
        self.DUMMY_PHONE_NUMBER = '1234567890'
        self.DUMMY_PASSWORD     = '1234567890'

        self.user = User(
            name         = self.DUMMY_NAME,
            email        = self.DUMMY_EMAIL,
            phone_number = self.DUMMY_PHONE_NUMBER,
            password     = self.DUMMY_PASSWORD
        )
        self.user.save()

    def tearsDown(self):
        pass

    def test_success(self):

        request = {
            'name'         : self.GOOD_NAME,
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'email'        : self.GOOD_EMAIL,
            'password'     : self.GOOD_PASSWORD
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'SUCCESS')
        self.assertEqual(response.status_code,201)

        self.assertEqual(User.objects.filter(name        =self.GOOD_NAME,\
                                             phone_number=self.GOOD_PHONE_NUMBER,\
                                             email       =self.GOOD_EMAIL).exists(),True)

    def test_check_get_necesser_keys(self):
        requests = []
        requests.append({
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'email'        : self.GOOD_EMAIL,
            'password'     : self.GOOD_PASSWORD
        })

        requests.append({
            'name'     : self.GOOD_NAME,
            'email'    : self.GOOD_EMAIL,
            'password' : self.GOOD_PASSWORD
        })

        requests.append({
            'name'         : self.GOOD_NAME,
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'password'     : self.GOOD_PASSWORD
        })

        requests.append({
            'name'         : self.GOOD_NAME,
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'email'        : self.GOOD_EMAIL,
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'KEY_ERROR')
            self.assertEqual(response.status_code,400)

    def test_check_email_vaildation(self):
        requests = []
        requests.append({
            'name'            : self.GOOD_NAME,
            'phone_number'    : self.GOOD_PHONE_NUMBER,
            'email'           : 'abcdefg.comi',
            'password'        : self.GOOD_PASSWORD
        })

        requests.append({
            'name'            : self.GOOD_NAME,
            'phone_number'    : self.GOOD_PHONE_NUMBER,
            'email'           : 'aaaaaaa@aaaaaa',
            'password'        : self.GOOD_PASSWORD
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'EMAIL_VALIDATION')
            self.assertEqual(response.status_code,400)

    def test_check_password_vaildation(self):
        requests = []
        requests.append({
            'name'         : self.GOOD_NAME,
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'email'        : self.GOOD_EMAIL,
            'password'     : '1234567'
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'PASSWORD_VALIDATION')
            self.assertEqual(response.status_code,400)

    def test_check_duplication(self):
        request = {
            'name'         : self.DUMMY_NAME,
            'email'        : self.DUMMY_EMAIL,
            'phone_number' : self.DUMMY_PHONE_NUMBER,
            'password'     : self.DUMMY_PASSWORD
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'DATA_ALREADY_EXIST')
        self.assertEqual(response.status_code,400)

    def test_authentication(self):

        request = {
            'name'         : self.GOOD_NAME,
            'phone_number' : self.GOOD_PHONE_NUMBER,
            'email'        : self.GOOD_EMAIL,
            'password'     : self.GOOD_PASSWORD
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'SUCCESS')

        hashed_password = User.objects.get(name=self.GOOD_NAME).password.encode('utf-8')
        new_password = self.GOOD_PASSWORD.encode('utf-8')

        self.assertEqual(bcrypt.checkpw(new_password, hashed_password),True)

class LoginTestCase(TestCase):
    def setUp(self):
        self.URL = '/user/login'
        self.SING_UP_URL = '/user/signup'
        self.client = Client()
        self.GOOD_NAME         = 'myname'
        self.GOOD_EMAIL        = 'abcdefg@gmail.com'
        self.GOOD_PHONE_NUMBER = '01012345678'
        self.GOOD_PASSWORD     = '12345678'

        self.DUMMY_NAME         = 'mr.dummy'
        self.DUMMY_EMAIL        = 'dummy@email.com'
        self.DUMMY_PHONE_NUMBER = '1234567890'
        self.DUMMY_PASSWORD     = '1234567890'

        request = {
            'name'         : self.DUMMY_NAME,
            'email'        : self.DUMMY_EMAIL,
            'phone_number' : self.DUMMY_PHONE_NUMBER,
            'password'     : self.DUMMY_PASSWORD
        }
        self.client.post(self.SING_UP_URL, request, content_type='application/json')
        # 인증 확인 용
        self.user = User.objects.get(name=self.DUMMY_NAME)
        self.access_token = jwt.encode({'id': self.user.pk}, settings.SECRET_KEY, algorithm = 'HS256').decode('utf-8')

    def tearsDown(self):
        pass

    def test_key_error(self):
        requests = []
        requests.append({
            'password' : self.GOOD_PASSWORD
        })

        requests.append({
            'account' : self.GOOD_NAME
        })

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'KEY_ERROR')
            self.assertEqual(response.status_code,400)

    def test_invalid_error(self):
        requests = []

        requests.append({
            'account'  : 'unknown',
            'password' : '1234567890'
        })

        requests.append({
            'account'  : '1234567890',
            'password' : 'unknown'
        })
        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'INVALID_USER')
            self.assertEqual(response.status_code,401)

    def test_success(self):
        requests = []

        requests.append({
            'account'  : self.DUMMY_NAME,
            'password' : self.DUMMY_PASSWORD
        })

        requests.append({
            'account'  : self.DUMMY_PHONE_NUMBER,
            'password' : self.DUMMY_PASSWORD
        })

        requests.append({
            'account'  : self.DUMMY_EMAIL,
            'password' : self.DUMMY_PASSWORD
        })

        user = User.objects.get(name=self.DUMMY_NAME)

        for request in requests:
            response = self.client.post(self.URL, request, content_type='application/json')
            self.assertEqual(response.json()['message'],'SUCCESS')
            self.assertEqual(response.status_code,200)

    def test_token(self):
        request = {
            'account'  : self.DUMMY_NAME,
            'password' : self.DUMMY_PASSWORD
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['authorization'], self.access_token)

class LoginDecoratorTestCase(TestCase):
    def setUp(self):
        # 어떤 SUCCESS를 반환해주는 함수를 만들고
        # Model DATA를 넣어 주고
        # 데코레이터 써서 invalid 확인
        # login해서 token 받을 필요있나?
        # 

        self.URL                = '/user/dummy'
        self.DUMMY_NAME         = 'mr.dummy'
        self.DUMMY_EMAIL        = 'dummy@email.com'
        self.DUMMY_PHONE_NUMBER = '1234567890'
        self.DUMMY_PASSWORD     = '1234567890'

        self.user = User(
            name         = self.DUMMY_NAME,
            email        = self.DUMMY_EMAIL,
            phone_number = self.DUMMY_PHONE_NUMBER,
            password     = self.DUMMY_PASSWORD
        )
        self.user.save()

        user = User.objects.get(name=self.DUMMY_NAME)
        self.user_id    = { 'id' : user.pk }
        self.unknown_id = { 'id' : 1234 }
        self.invalid_id = { 'i'  : user.pk}

        self.good_token    = jwt.encode(self.user_id,
                                        settings.SECRET_KEY,
                                        algorithm=settings.ALGORITHM
                                        ).decode('utf-8')

        self.unknown_token  = jwt.encode(self.unknown_id,
                                        settings.SECRET_KEY,
                                        algorithm=settings.ALGORITHM
                                        ).decode('utf-8')

        self.invalid_token = jwt.encode(self.invalid_id,
                                        settings.SECRET_KEY,
                                        algorithm=settings.ALGORITHM
                                       ).decode('utf-8')

        self.body = {}

    def test_success(self):
        header = {
            'HTTP_Authorization' : self.good_token,
        }
        response = self.client.post(self.URL, self.body, content_type='application/json', **header)
        self.assertEqual(response.json()['message'],'SUCCESS')

    def test_invail_token(self):
        header = {
            'unknown_value' : self.good_token,
        }
        response = self.client.post(self.URL, self.body, content_type='application/json', **header)
        self.assertEqual(response.json()['message'],'DO_NOT_EXIST_TOKEN')

    def test_not_exist_user(self):
        header = {
            'HTTP_Authorization' : self.unknown_token,
        }
        response = self.client.post(self.URL, self.body, content_type='application/json', **header)
        self.assertEqual(response.json()['message'],'DO_NOT_EXIST_USER')

    def test_key_error_id(self):
        header = {
            'HTTP_Authorization' : self.invalid_token,
        }
        response = self.client.post(self.URL, self.body, content_type='application/json', **header)
        self.assertEqual(response.json()['message'],f'INVALID_TOKEN:{self.invalid_id}')

    def test_decode_error(self):
        header = {
            'HTTP_Authorization' : 1 ,
        }
        response = self.client.post(self.URL, self.body, content_type='application/json', **header)
        self.assertEqual(response.json()['message'],f'INVALID_TOKEN: TYPE_ERROR')

