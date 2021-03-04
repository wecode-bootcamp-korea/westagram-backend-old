import os
import sys
import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

sys.path.append(os.path.dirname(__file__))
from user.models    import User
from post.models    import Post

class PostView(View):
    def post(self, request):
        data            =   json.loads(request.body)
        phone_number    =   data.get('phone_number', None)
        email_adress    =   data.get('email_adress', None)
        nickname        =   data.get('nickname', None)
        content         =   data['content']
        image_url       =   data['image_url']

        try:
            if User.objects.filter(
                                    Q(phone_number  =   phone_number)|
                                    Q(email_adress  =   email_adress)|
                                    Q(nickname      =   nickname)
                                ).exists():
                user = User.objects.get(
                                    Q(phone_number  =   phone_number)|
                                    Q(email_adress  =   email_adress)|
                                    Q(nickname      =   nickname)
                        )
                Post(
                        user        =   user,
                        content     =   content,
                        image_url   =   image_url
                        ).save()
                return JsonResponse({'message':'SUCESS'}, status = 200)
            return JsonResponse({'message':'UNATHORIZED'}, status = 401)
        
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class PostDisplayView(View):
    def get(self, request):
        post_data = Post.objects.values()
        return JsonResponse({'post_data': list(post_data)}, status = 200)
