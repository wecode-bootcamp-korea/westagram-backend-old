import json

from django.views import View
from django.http  import JsonResponse
from django.core  import serializers

from User.models import User
from .models     import Post

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        if 'user' in data.keys() and 'img_url' in data.keys():
            user    = data['user']
            img_url = data['img_url']
        else:
            return JsonResponse({'message':'User and ImgUrl are neccesary'}, status = 400)

        if not User.objects.filter(email = user):
            return JsonResponse({'message':'You did not join'}, status = 400)
        else:
            user = User.objects.get(email = user)

        if 'content' in data.keys():
            content = data['content']
        else:
            content = ""

        Post(
            user    = user,
            img_url = img_url,
            content = content
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class GetView(View):
    def get(self, request):
        post = Post.objects.all()

        return JsonResponse(serializers.serialize('json', post),safe = False, status = 200)
