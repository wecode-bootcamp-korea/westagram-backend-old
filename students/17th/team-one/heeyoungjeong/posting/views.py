import json
import jwt
import my_settings
from utils import login_decorator

from json.decoder import JSONDecodeError
from jwt import InvalidSignatureError
from posting.models import Posting
from posting.models import User


from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


SECRET_KEY = my_settings.SECRET_KEY['secret']


class PostingView(View):
    @login_decorator
    def post(self, request):

        try:
            data = json.loads(request.body)
            user = request.user

            title = data.get('title', None)
            content = data.get('content', None)
            image_url = data.get('image_url', None)
            ACCESS_TOKEN = data.get('ACCESS_TOKEN', None)
            # print("'"+ACCESS_TOKEN+"'")
            # ACCESS_TOKEN = ACCESS_TOKEN.encode('utf-8')

            if not (title and content and image_url and ACCESS_TOKEN):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # payload = jwt.decode(ACCESS_TOKEN, SECRET_KEY, algorithms='HS256')
            # print(payload)
            # user = User.objects.get(id=payload['user_id'])
            # if not user:
            #     return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)

            Posting.objects.create(
                user_id=user.id,
                title=title,
                content=content,
                image_url=image_url,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except InvalidSignatureError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=401)
