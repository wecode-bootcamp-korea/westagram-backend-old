import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from accounts.models import User
from .models import Post

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(phone_number=data['phone_number'])
            post = Post(
                author = user,
                contents = data['contents'],
                image_url = data['image_url'],
            ).save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except:
            return JsonResponse({'message' : 'FAILED'}, status = 400)

class PostListView(View):
    def get(self, request):
        posts = Post.objects.all().values()
        posts_list = list(posts)
        return JsonResponse(posts_list, safe = False)

