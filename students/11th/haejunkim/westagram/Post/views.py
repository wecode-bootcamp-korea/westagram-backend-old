import json

from django.views           import View
from django.http            import JsonResponse

from User.models import User
from .models     import Post


class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(id = data['user_id']).exists():
                email = User.objects.get(id = data['user_id'])
                Post(
                    email     = email,
                    content   = data['content'],
                    image_url = data['image_url'],
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
        except Exception as e:
            return JsonResponse({'message' : f'{e}'}, status = 400)

class PostDisplayView(View):
    def get(self, request):
        post_data = Post.objects.values()
        return JsonResponse({'post_data' : list(post_data)}, status = 200)
