import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import Post
from my_settings import SECRET_KEY, ALGORITHM

class Posting(View):
    def post(self, request):
        data = json.loads(request.body)

        user      = data['user']
        image_url = data['image_url']
        content   = data['content']
        
        Post.objects.create(user=user, image_url=image_url, content=content)
        return JsonResponse({'message':'SUCCESS'}, status = 200)

