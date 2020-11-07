import json

from django.test import TransactionTestCase
from django.urls import reverse
from django.db import connection
from django.utils import timezone

class TestPost(TransactionTestCase):
    def setUp(self):
        data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url = reverse('user')
        reponse = self.client.post(url, data=json.dumps(data), content_type='application/json')
        
        data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url = reverse('user')
        response = self.client.post(url, data=json.dumps(data_2), content_type='application/json')
    
    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('set foreign_key_checks=1')
            
    def test_create_post(self):
        data = {
            'user_id'   : 1,
            'content'   : 'ㄴ ㅏ는 ㄱ ㅏ끔 눈물을 흘린ㄷ ㅏㅠ',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    def test_fail_create_post_no_id(self):
        data = {
            'content'  : '도우너 어서 오고',
            'image_url': 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_post_no_image(self):
        data = {
            'user_id' : 2,
            'content' : '어이 둘리'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_post_no_content(self):
        data = {
            'user_id'   : 1,
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_too_many_key(self):
        data = {
            'user_id'   : 1,
            'content'   : '처신 잘하라고',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg',
            'phone'     : '01012341234'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_not_image_url(self):
        data = {
            'user_id'   : 1,
            'content'   : '초능력 맛 좀 볼래?',
            'image_url' : 'asdf@naver.com'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'BAD_IMAGE_URL_REQUEST'

    def test_fail_create_user_not_exist(self):
        data = {
            'user_id'   : 3,
            'content'   : '졸려...',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'
    
    def test_get_posts(self):
        create_data = {
            'user_id'   : 2,
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json')
        assert response.status_code == 200
        
        create_data_2 = {
            'user_id'   : 1,
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json')
        assert response.status_code == 200

        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['posts'] == [
            {
                'name'       : 'douner',
                'content'    : '어이 둘리',
                'image_url'  : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                'name'       : 'dooly',
                'content'    : '도우너 어서 오고',
                'image_url'  : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]

    def test_get_no_post(self):
        url = reverse('post')
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'None_post_data'

class TestComment(TransactionTestCase):
    def setUp(self):
        data = {
            'name'     : 'dooly',
            'password' : '123456qwerT*',
            'phone'    : '01012341234',
            'email'    : 'dooly@naver.com'
        }
        url = reverse('user')
        reponse = self.client.post(url, data=json.dumps(data), content_type='application/json')
        
        data_2 = {
            'name'     : 'douner',
            'password' : '123456asdf*E',
            'phone'    : '01043214321',
            'email'    : 'douner@naver.com'
        }
        url = reverse('user')
        response = self.client.post(url, data=json.dumps(data_2), content_type='application/json')
    
        create_data = {
            'user_id'   : 2,
            'content'   : '어이 둘리',
            'image_url' : 'http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg'
        }
        url = reverse('post')
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json')
        assert response.status_code == 200
        
        create_data_2 = {
            'user_id'   : 1,
            'content'   : '도우너 어서 오고',
            'image_url' : 'https://topclass.chosun.com/news_img/1807/1807_008_1.jpg'
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json')
        assert response.status_code == 200

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate users')
            cursor.execute('truncate posts')
            cursor.execute('set foreign_key_checks=1')
 
    def test_create_comment(self):
        url = reverse('comment') 
        create_data = {
            'user_id' : 2,
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json')
        assert response.status_code == 200

    def test_fail_create_comment_no_id(self):
        url = reverse('comment')
        fail_data = {
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_comment_no_post(self):
        url = reverse('comment')
        fail_data = {
            'user_id' : 2,
            'comment' : '깐따삐야'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_comment_no_comment(self):
        url = reverse('comment')
        fail_data = {
            'user_id' : 2,
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'KEY_ERROR'

    def test_fail_create_user_not_exist(self):
        url = reverse('comment')
        fail_data = {
            'user_id' : 3,
            'post_id' : 2,
            'comment' : 'ㅋㅋㅋ'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 401
        assert json.loads(response.content)['message'] == 'INVALID_USER'

    def test_fail_create_post_not_found(self):
        url = reverse('comment')
        fail_data = {
            'user_id' : 2,
            'post_id' : 5,
            'comment' : 'ㅎㅎㅎㅎㅎㅎ'
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'

    def test_fail_create_too_long_text(self):
        url = reverse('comment')
        fail_data = {
            'user_id' : 2,
            'comment' : 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(fail_data), content_type='application/json')
        assert response.status_code == 400
        assert json.loads(response.content)['message'] == 'TOO_LONG_COMMENT'

    def test_get_comment(self):
        url = reverse('comment') 
        create_data = {
            'user_id' : 2,
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json')
        assert response.status_code == 200

        create_data_2 = {
            'user_id' : 1,
            'comment' : '어서 오고',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json')
        assert response.status_code == 200

        url = reverse('comment_list', args=[2]) 
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['comments'] == [
            {
                'name'       : 'douner',
                'comment'    : '깐따삐야',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H : %M : %S')
            },{
                'name'       : 'dooly',
                'comment'    : '어서 오고',
                'created_at' : timezone.now().strftime('%Y-%m-%d %H : %M : %S')
            }
        ]

    def test_get_comment_is_None(self):
        url = reverse('comment') 
        create_data = {
            'user_id' : 2,
            'comment' : '깐따삐야',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data), content_type='application/json')
        assert response.status_code == 200

        create_data_2 = {
            'user_id' : 1,
            'comment' : '어서 오고',
            'post_id' : 2
        }
        response = self.client.post(url, data=json.dumps(create_data_2), content_type='application/json')
        assert response.status_code == 200

        url = reverse('comment_list', args=[1])
        response = self.client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)['message'] == 'None_comment_data'

    def test_fail_get_comment_post_not_found(self):
        url = reverse('comment_list', args=[100])
        response = self.client.get(url)
        assert response.status_code == 404
        assert json.loads(response.content)['message'] == 'POST_NOT_FOUND'
