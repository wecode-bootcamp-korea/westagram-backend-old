import json

from django.http   import JsonResponse
from django.views  import View

from user.models   import User
from .models       import Post

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id=data['user']).exists():
                user = User.objects.get(id= data['user'])
                Post.objects.create(
                    user = user,
                    content = data['content'],
                    img_url = data['img_url']
                )
                return JsonResponse({'MESSAGE' : 'SUCCES'}, status = 200)
            return JsonResponse({'MESSAGE' : 'UPLOAD ERROR'}, status = 400)

        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KEYERROR'}, status = 400)
           
class GetView(View):
    # def get(self, request):
    #     data = json.loads(request.body)
    #     posts = Post.objects.all()
    #     post_list = []
    #     for post in posts:
    #         post_list.append(post)
    #     return JsonResponse({'MESSAGE' : post_list}, status = 200)
    def get(self, request):
        posts = Post.objects.values()
        return JsonResponse({'posts' : list(posts)}, status = 200)

            