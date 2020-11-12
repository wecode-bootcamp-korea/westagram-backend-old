import json

from django.urls import reverse
from django.test import TransactionTestCase
from django.db import connection

from user.models import User

class TestView(TransactionTestCase):
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

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate follow_lists')
            cursor.execute('truncate posts')
            cursor.execute('truncate comments')
            cursor.execute('set foreign_key_checks=1')

    def test_fail_create_no_name(self):
        url  = reverse('sign_up')
        data = {
            'password' : '123453*$G',
            'phone'    : '11122223333',
            'email'    : 'min@naver.com'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_password(self):
        url  = reverse('sign_up')
        data = {
            'name'  : 'min',
            'phone' : '11122223333',
            'email' : 'min@naver.com' }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_email(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'phone'    : '11122223333',
            'password' : '123456*IW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_no_phone(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123456*RE'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'
    
    def test_fail_create_wrong_name(self):
        url  = reverse('sign_up')
        data = {
            'name'     : '"@S2zl존전사S2@" ',
            'email'    : 'min@naver.com',
            'password' : '1234#Fe32@',
            'phone'    : '01011112222'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == "BAD_NAME_REQUEST"

    def test_fail_create_wrong_email(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'email'    : 'fjskdlw.com',
            'password' : '13245*ISD',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == "BAD_EMAIL_REQUEST"
    
    def test_fail_create_wrong_password(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '1',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PASSWORD_REQUEST'

    def test_fail_create_too_short_phone_number(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123werEOE*',
            'phone'    : '000111111'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PHONE_NUMBER_REQUEST'
    
    def test_fail_create_wrong_phone_number(self):
        url  = reverse('sign_up')
        data = {
            'name'     : 'min',
            'email'    : 'min@naver.com',
            'password' : '123qwerER-#$',
            'phone'    : 'skdjfi1234'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_PHONE_NUMBER_REQUEST'

    def test_fail_create_user_exists(self):    
        url  = reverse('sign_up')
        data = {
            'name'     : 'kim',
            'email'    : 'min@naver.com',
            'password' : '123456EU**',
            'phone'    : '11122223333'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'USER_EXISTS'

    def test_name_login(self):
        url  = reverse('login')
        data = {
            'name'     : 'kim',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert 'access_token' in json.loads(response.content) 
    
    def test_email_login(self):
        url  = reverse('login')
        data = {
            'email'    : 'kim@naver.com',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert  response.status_code == 200
        assert 'access_token' in json.loads(response.content) 

    def test_phone_login(self):
        url  = reverse('login')
        data = {
            'phone'    : '01033334444',
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert 'access_token' in json.loads(response.content) 

    def test_fail_login_wrong_user(self):
        url  = reverse('login')
        data = {
            'name'     : 'lee',
            'password' : '123455'
        }
        response = self.client.post(url, data=json.dumps(data),content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_login_wrong_password(self):
        url  = reverse('login')
        data = {
            'name'     : 'kim',
            'password' : '123'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_login_no_password(self):
        url  = reverse('login')
        data = {
            'name' : 'kim'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_login_no_id(self):
        url  = reverse('login')
        data = {
            'password' : '123456W*weW'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

class TestFollow(TransactionTestCase):
    def setUp(self):
        data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        
        data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url      = reverse('sign_up')
        response = self.client.post(url, data=json.dumps(data_2), content_type='application/json')
        
        login_data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*'
        }
        url                 = reverse('login')
        response            = self.client.post(url, data=json.dumps(login_data), content_type='application/json')
        self.access_token_1 = json.loads(response.content)['access_token']

        login_data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E'
        }
        response            = self.client.post(url, data=json.dumps(login_data_2), content_type='application/json')
        self.access_token_2 = json.loads(response.content)['access_token']

        create_data = {
            'user_id'   : 2,
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
            
        }
        url            = reverse('post')
        self.headers_1 = {
            'HTTP_Authorization' : self.access_token_1
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json',  **self.headers_1 )

        create_data_2 = {
            'user_id'   : 1,
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        self.headers_2 = {
            'HTTP_Authorization' : self.access_token_2
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json', **self.headers_2)

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('truncate follow_lists')
            cursor.execute('set foreign_key_checks=1')

    def test_add_follow(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 2,
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url  = reverse('follow')
        data = {
            'follow_id' : 1,
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_2)
        assert response.status_code == 200

    def test_fail_add_follow_no_token(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'
    
    def test_fail_add_follow_wrong_follow_id(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 5
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_add_follow_already_following(self):
        url         = reverse('follow')
        create_data = {
            'follow_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

        url       = reverse('follow')
        fail_data = {
            'follow_id' : 2
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json', **self.headers_1)
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'THIS_USER_ALREADY_FOLLOING'

    def test_delete_follow(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 2
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200
        
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 200

    def test_fail_delete_follow_no_id(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 2
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_delete_follow_wrong_follow_id(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 100
        }
        response = self.client.delete(url, data=json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_delete_follow_not_follow(self):
        url  = reverse('follow')
        data = {
            'follow_id' : 2
        }
        response = self.client.delete(url, json.dumps(data), content_type='application/json', **self.headers_1)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'USER_NOT_FOLLOWED'

