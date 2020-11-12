import json
import ipdb
import jwt

from django.test import TestCase, Client
from django.shortcuts import reverse

from user.models import User
# Create your tests here.

client = Client()
class resgister(TestCase):

    def test_register_user_success(self):

        data = {
            'username':'amuse',
            'email':'amusesla@gmail.com',
            'password':'wecode1234',
            'phone_number':'010-5752-9507'
        }

        response = client.post('/user/register', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content),{'message' : 'SUCCESS'})


class Login(TestCase):

    def setUp(self):
        data = {
            'username':'amuse',
            'email':'amusesla@gmail.com',
            'password':'wecode1234',
            'phone_number':'010-5752-9507'
        }

        client.post(reverse('user:register'), json.dumps(data), content_type='application/json')

    def test_login_success(self):
        data = {
            'key':'amuse',
            'password':'wecode1234'
        }


        response = client.post('/user/login', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

class Post_create(TestCase):
    def setUp(self):
        data = {
            'username':'amuse',
            'email':'amusesla@gmail.com',
            'password':'wecode1234',
            'phone_number':'010-5752-9507'
        }

        client.post('/user/register', json.dumps(data), content_type='application/json')

        data = {
            'key':'amuse',
            'password':'wecode1234'
        }

        response = client.post('/user/login', json.dumps(data), content_type='application/json')
        self.token = json.loads(response.content)['access_token']

    def test_craete_post(self):
        #Client(HTTP_AUTHORIZATION=self.token)
        header={'HTTP_Authorization': self.token}
        data = {
            'title':'FIRST BLOG POST TITLE',
            'content':'learning django in wecode academy',
            'img_url':'http://www.imageurl.com'
        }
        response = client.post('/post/', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(json.loads(response.content), {'message':'POST HAS BEEN CREATED SUCCESSFULLY!'})
        self.assertEqual(response.status_code, 201)

#class Comment_create(TestCase):
#    def SetUp(self):
#        data={
#            'username':'amuse',
#            'email':'amusesla@gmail.com',
#            'password':'wecode1234',
#            'phon_number':'010-5752-9507'
#        }
#        #데이터베이스에 유저 생성
#        client.post('/user/register', json.dumps(data), content_type= 'application/json')
#        #content_type 을 명시하지 않으면 자동으로 x-www-from-urlendcoded default값으로 설정되기때문에 꼭첨부..!
#
#        #로그인 입력 data
#        data = {
#            'key':'amuse',
#            'password':'wecode1234'
#        }
#        
#        # response 변수에 response(client.post 결과) 담아준다.
#        response = client.post('/user/login', json.dumps(data), content_type = 'application/json')
#        # 토큰값을 token 변수에 참조해준다.
#        self.token = json.loads(response.content)['access_token']
#
#
#        data = {
#            'author':'1',
#            'title': ,
#            'content': ,
#            'image_url': 
#        }
#
#
#
