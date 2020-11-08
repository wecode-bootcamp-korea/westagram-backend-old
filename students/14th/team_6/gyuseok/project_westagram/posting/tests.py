from django.test import TestCase, Client
from user.models import User
from .models     import Post

class RegisterTestCase(TestCase):
    def setUp(self):
        self.URL = '/posting/register/'
        self.client = Client()

        self.DUMMY_NAME         = 'mr.dummy'
        self.DUMMY_EMAIL        = 'dummy@email.com'
        self.DUMMY_PHONE_NUMBER = '1234567890'
        self.DUMMY_PASSWORD     = '1234567890'

        self.DUMMY_CONTENT      = 'unknown_content'
        self.DUMMY_IMAGE_URL    = 'unknown_image_url'

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
            'username'  : self.DUMMY_NAME,
            'content'   : self.DUMMY_CONTENT,
            'image_url' : self.DUMMY_IMAGE_URL,
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'SUCCESS')
        self.assertEqual(response.status_code,200)

        user_key = User.objects.get(name=self.DUMMY_NAME)
        self.assertEqual(Post.objects.filter(user = user_key).exists(),True)

    def test_not_exist(self):
        request = {
            'username'  : 'anonymous',
            'content'   : self.DUMMY_CONTENT,
            'image_url' : self.DUMMY_IMAGE_URL,
        }

        response = self.client.post(self.URL, request, content_type='application/json')
        self.assertEqual(response.json()['message'],'NOT EXIST USER')
        self.assertEqual(response.status_code,400)

