import json

from django.http      import JsonResponse
from django.views     import View
from utils.decorators import LoginCahsed

from .models import Post


class CreatePostView(View):
    @LoginCahsed
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            [title, content, image_url] = data.values()
            
            Post.objects.create(
                author = request.user, title = title, content = content, image_url=image_url
            )

            return JsonResponse({
                'message': 'POST_SUCCESSFULLY_CREATED',
            }, status=200)
        
        except KeyError:
            return JsonResponse({
                'message': 'KEY_ERROR',
            }, status=400)
            
            

            
            
            
        
