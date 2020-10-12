import json

from django.views   import View
from django.http    import JsonResponse
from posting.models import Post
from user.models    import User


class PostView(View):
    def post(self,request):
       # try:
        data = json.loads(requst.body)
        User (
                user = data['user'],
                img_url = data['img_url']
                ).save()
        return JsonResponse({'message':data},status=200)

