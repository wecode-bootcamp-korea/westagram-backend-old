from django.test import TestCase, Client
from posts.models import Post
from users.models import User

clinet = Client()
class JustTest(TestCase):

    def setUp(self):
       print("--------------- setUp -----------------")
       user = User.objects.create(email = "jun@email.com", password = "wecode123")
       Post.objects.create(user = user, content = "고양이인가", image_url = "haha.jpg")
    
    def test_check_post(self):
        print("--------------- check_psot -----------------")
        post = Post.objects.get(id = 4)
        self.assertEqual(post.content, "고양이인가")
