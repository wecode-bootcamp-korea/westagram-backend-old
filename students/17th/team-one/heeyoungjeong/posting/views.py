import json
import jwt
import my_settings


from json.decoder import JSONDecodeError
from jwt import InvalidSignatureError
from posting.models import Posting
from posting.models import User


from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


SECRET_KEY = my_settings.SECRET_KEY['secret']

"""
1. post로 데이터를 받는다.
2. 데이터 검증한다
2. 값을 저장한다.
3. 회원가입과 로그인이 되어있는지 먼저 판별해야한다.(토큰이용)

    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    image_url = models.URLField(null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
"""
class PostingView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            title = data.get('title', None)
            content = data.get('content', None)
            image_url = data.get('image_url', None)
            ACCESS_TOKEN = data.get('ACCESS_TOKEN', None)
            # print("'"+ACCESS_TOKEN+"'")
            # ACCESS_TOKEN = ACCESS_TOKEN.encode('utf-8')

            if not (title and content and image_url and ACCESS_TOKEN):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            payload = jwt.decode(ACCESS_TOKEN, SECRET_KEY, algorithms='HS256')
            print(payload)
            user = User.objects.get(id=payload['user_id'])
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            Posting.objects.create(
                user_id=payload['user_id'],
                title=title,
                content=content,
                image_url=image_url,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST222'}, status=400)

        except InvalidSignatureError:
            return JsonResponse({'message': 'BAD_REQUEST1111'}, status=401)
