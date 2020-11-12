import json
import jwt

from django.test import TestCase, Client
from django.conf import settings

from user.models import User
from .models     import Post

class BoardTestCase(TestCase):
    def setUp(self):
        self.URL = '/posting/board'
        self.client = Client()

        self.DUMMY_NAME         = 'mr.dummy'
        self.DUMMY_EMAIL        = 'dummy@email.com'
        self.DUMMY_PHONE_NUMBER = '1234567890'
        self.DUMMY_PASSWORD     = '1234567890'

        self.DUMMY_CONTENT      = 'unknown_content'
        self.DUMMY_IMAGE_URL    = 'unknown_image_url'

        self.user = User.objects.create(
            name         = self.DUMMY_NAME,
            email        = self.DUMMY_EMAIL,
            phone_number = self.DUMMY_PHONE_NUMBER,
            password     = self.DUMMY_PASSWORD
        )
        self.user.save()

        user = User.objects.get(name=self.DUMMY_NAME)
        self.DUMMY_AUTH = jwt.encode({'id':user.pk}, 
                                     settings.SECRET_KEY,
                                     algorithm=settings.ALGORITHM
                                     ).decode('utf-8')

        self.header = {
            'HTTP_Authorization': self.DUMMY_AUTH,
        }

    def tearsDown(self):
        pass

    def test_success(self):

        user = User.objects.get(name=self.DUMMY_NAME)
        request = {
            'content'      : self.DUMMY_CONTENT,
            'image_url'    : self.DUMMY_IMAGE_URL,
        }

        response = self.client.post(self.URL, request, content_type='application/json', **self.header)
        self.assertEqual(response.json()['message'], 'SUCCESS')
        self.assertEqual(response.status_code,201)

        user_key = User.objects.get(name=self.DUMMY_NAME)
        self.assertEqual(Post.objects.filter(user = user_key).exists(),True)

