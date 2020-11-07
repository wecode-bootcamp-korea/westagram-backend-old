import json

from django.urls import reverse
from django.test import TestCase

from user.models import User

class TestView(TestCase):
    def setUp(self):
        user_name = 'kim'
        password  = '123456W*weW'
        phone     = '01033334444'
        email     = 'kim@naver.com'

        url  = reverse('sign_up')
        data = {
            'name'     : user_name,
            'password' : password,
            'phone'    : phone,
            'email'    : email
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        
    def test_fail_create_no_name(self):
        url = reverse('sign_up')
        fail_data = {
            'password' : '123453*$G',
            'phone'    : '11122223333',
            'email'    : 'min@naver.com'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_password(self):
        url = reverse('sign_up')
        fail_data = {
            'name'  : 'min',
            'phone' : '11122223333',
            'email' : 'min@naver.com' }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_email(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'phone'    : '11122223333',
            'password' : '123456*IW'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_phone(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123456*RE'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'
    
    def test_fail_create_wrong_name(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : '"@S2zl존전사S2@" ',
            'email'    : 'min@naver.com',
            'password' : '1234#Fe32@',
            'phone'    : '01011112222'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == "BAD_NAME_REQUEST"

    def test_fail_create_wrong_email(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'email'    : 'fjskdlw.com',
            'password' : '13245*ISD',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == "BAD_EMAIL_REQUEST"
    
    def test_fail_create_wrong_password(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '1',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PASSWORD_REQUEST'

    def test_fail_create_too_short_phone_number(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123werEOE*',
            'phone'    : '000111111'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PHONE_NUMBER_REQUEST'
    
    def test_fail_create_wrong_phone_number(self):
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123qwerER-#$',
            'phone'    : 'skdjfi1234'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PHONE_NUMBER_REQUEST'

    def test_fail_create_user_exists(self):    
        url = reverse('sign_up')
        fail_data = {
            'name'     : 'kim',
            'email'    : 'min@naver.com',
            'password' : '123456EU**',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'USER_EXISTS'

    def test_name_login(self):
        url = reverse('login')
        data = {
            'name'     : 'kim',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
    
    def test_email_login(self):
        url = reverse('login')
        data = {
            'email'    : 'kim@naver.com',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert  response.status_code == 200

    def test_phone_login(self):
        url = reverse('login')
        data = {
            'phone'    : '01033334444',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
    
    def test_fail_login_wrong_user(self):
        url = reverse('login')
        fail_data = {
            'name'     : 'lee',
            'password' : '123455'
        }
        response = self.client.post(url, data=json.dumps(fail_data),content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_login_wrong_password(self):
        url = reverse('login')
        fail_data = {
            'name'     : 'kim',
            'password' : '123'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_login_no_password(self):
        url = reverse('login')
        fail_data = {
            'name' : 'kim'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_login_no_id(self):
        url = reverse('login')
        fail_data = {
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_login_too_many_key(self):
        url = reverse('login')
        fail_data = {
            'name'     : 'kim',
            'email'    : 'kim@naver.com',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'


