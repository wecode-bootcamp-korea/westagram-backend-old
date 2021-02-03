import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post
from user.models  import User
from utils        import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        data      = json.loads(request.body)
        user      = request.user
        image_url = data.get('image_url', None)
        content   = data.get('content', None)
        
        # KEY_ERROR check
        if not image_url:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
        post = Post.objects.create(
            user      = user,
            image_url = image_url,
            content   = content
        )

        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def get(self, request):
        post_list = [{
                'user'      : post.user.name,
                'image_url' : post.image_url,
                'content'   : post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
            } for post in Post.objects.all()
        ]

        return JsonResponse({'data': post_list}, status=200)

