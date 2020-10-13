import json
import re
import datetime
from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse
from .models          import User
from .models          import Post

class CreatePost(View):
    def post(self, request):
        data    = json.loads(request.body)
        name_id    = data['name_id']
        time    = datetime.datetime.now()
        image_url   = data['image_url']
        content = data['content']

        Post.objects.create(
            name_id        = name_id,
            time        = time,
            image_url   = image_url,
            content     = content
            )

        return JsonResponse({'message' : 'Posted! '}, status=200)
            
        
class GetPost(View):
    def get(self, request):
        data    = json.loads(request.body)
        user    = data['name']
        posts   = Post.objects.all().values()
        get_posts = []

        for post in posts:
            get_posts.append(post)

        return JsonResponse({'message' : 'Posts'}, status=200)    