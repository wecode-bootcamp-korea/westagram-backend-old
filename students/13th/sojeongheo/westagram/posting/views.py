import json
import jwt

from django.views   import View
from django.http    import HttpResponse, JsonResponse

from posting.models import Posting
from user.models    import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        Posting.objects.create(
            user_id     = data['user_id'],
            img_url     = data['img_url'],
            contents    = data['contents']
        )
            
        return JsonResponse({"message": "SUCCESS"}, status=201)
       
    def get(self, request):
        posts = Posting.objects.values()
        postfeed = [post for post in posts]

        return JsonResponse({"posts": postfeed}, status=200)
