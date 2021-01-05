import json
import re

from django.http  import JsonResponse
from django.views import View

from .models     import Post
from user.models import User

class PostView(View):

    def post(self, request):

        try:
            data    = json.loads(request.body)
            email   = data.get('email')
            phone   = data.get('phone')
            img     = data['img']
            content = data.get('content')

            if email is not None and phone is None:
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    Post.objects.create(user=user, img=img, content=content)
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                return JsonResponse({"message":"INVALID_USER"}, status=401)

            elif phone is not None and email is None:
                if User.objects.filter(phone=phone).exists():
                    user = User.objects.get(phone=phone)
                    Post.objects.create(user=user, img=img, content=content)
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                return JsonResponse({"message":"INVALID_USER"}, status=401)

            else:
                return JsonResponse({"message":"INVALID_DATA"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
#        except:
#            return JsonResponse({"message": "ERROR"}, status=500)
#
    def get(self, request):
        posts = Post.objects.all()
        post_list = []
        for post in posts:
            post_list.append({
                'user_id'    : post.id,
                'content'    : post.content,
                'img'        : post.img,
                'created_dt' : post.created_dt
            })
        return JsonResponse({"posts": post_list}, stauts=200)
