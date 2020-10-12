import json

from django.views   import View
from django.http    import JsonResponse
from posting.models import Post
from user.models    import User


class PostView(View):
    def post(self,request):
       # try:
        data = json.loads(request.body)
        user = data['user']
        a = User.objects.get(name=user)
        #return JsonResponse({'message':user},status=201)

        return JsonResponse({"user_name": a.name}, status=201)

