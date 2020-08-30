import json

from django.views           import View
from django.http            import JsonResponse

from User.models import User
from User.utils  import login_required
from .models     import (
    Post,
    Comment
)

class PostView(View):
    @login_required
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
    @login_required
    def get(self, request):
        post_data = Post.objects.values()
        return JsonResponse({'post_data' : list(post_data)}, status = 200)

class CommentView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(id = data['user_id']).exists() and Post.objects.filter(id = data['post_id']).exists():
                Comment(
                    email       = User.objects.get(id = data['user_id']),
                    post        = Post.objects.get(id  = data['post_id']),
                    comment     = data['comment'],
                    created_at  = data['created_at']
                ).save()
                return JsonResponse({"message" : "SUCCESS"}, status = 200)

            return JsonResponse({"message" : "USER OR POST DOES NOT EXIST"}, status = 400)
        except Exception as e:
            return JsonResponse({"message" : f'{e}'}, status = 400)

class  CommentDisplayView(View):
    @login_required
    def get(self, request, post_id):
        db_comment   = Comment.objects.all().values()
        comment_list = list(db_comment)
        return JsonResponse(comment_list, safe = False)
