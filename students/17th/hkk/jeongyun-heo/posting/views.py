import json

from django.http     import JsonResponse
from django.views    import View

from user.models import User
from .models import Post

class PostView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            image_url = data['image_url']
            content   = data['content']
            
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            user = User.objects.get(email=email)

            Post.objects.create(user=user, image_url=image_url, content=content)

            return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
            posts = Post.objects.all()
            post_list = []            
            for post in posts:
                post_list.append(
                    {
                    'user_name' : post.user.name,
                    'image_url' : post.image_url,
                    'content'   : post.content,
                    'created_at': post.created_at
                    }
                                ) 
            return JsonResponse({'posts': post_list}, status=200)