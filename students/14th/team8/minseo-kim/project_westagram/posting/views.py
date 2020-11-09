import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Post
from user.models import User

class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message':'INVALID_USER'},status=401)

            Post.objects.create(
                image_url=data['image_url'],
                user_id=data['user_id'],
                content=data['content']
            )

            return JsonResponse({'message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

class DisplayPostView(View):
    def get(self,request):
        user_posts = Post.objects.all()
        if user_posts.exists():
            posts = []

            for user_post in user_posts:
                posts.append({
                    'name':User.objects.filter(id=user_post.user_id)[0].name,
                    'created_time': user_post.created_time,
                    'content': user_post.content,
                    'image_url': user_post.image_url
                })

            return JsonResponse({'result':posts}, status=200)

        else:
            return JsonResponse({'message':'NO_CONTENT'},status=404)


