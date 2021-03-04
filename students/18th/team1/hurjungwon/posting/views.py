import json

from django.views import View
from django.http  import JsonResponse

from account.models import User
from .models        import Post


class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:

            user_name = User.objects.get(user_name=data['user_name'])
            user_id   = user_name.id

            Post.objects.create(
                image_url    = data['img_url'],
                content      = data['content'],
                user_name_id = user_id
            )
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        else:
            return JsonResponse({'message': 'SUCCSESS'}, status=200)
            
    def get(self, request):
        posts = Post.objects.all()
        
        result = []
        
        for post in posts:
            user_id   = post.user_name
            user_name = user_id.user_name
            
            post_dict = {
                'user_name'  : user_name,
                'image_url'  : post.image_url,
                'content'    : post.content,
                'create_date': post.create_date,
            }
            result.append(post_dict)

        return JsonResponse({'result': result}, status=200)