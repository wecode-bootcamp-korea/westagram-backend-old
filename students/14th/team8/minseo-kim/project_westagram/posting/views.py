import json

from django.http import JsonResponse
from django.views import View

from .models import Post, Comment
from user.models import User

class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message':'INVALID_USER'},status=401)

            Post.objects.create(
                image_url = data['image_url'],
                user_id   = data['user_id'],
                content   = data.get('content')
            )
            print(data.get('content'))

            return JsonResponse({'message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

    def get(self,request):
        user_posts = Post.objects.all()
        if user_posts.exists():
            posts = []

            for user_post in user_posts:
                posts.append({
                    'name'         : User.objects.filter(id=user_post.user_id)[0].name,
                    'created_time' : user_post.created_time,
                    'content'      : user_post.content,
                    'image_url'    : user_post.image_url
                })

            return JsonResponse({'result':posts}, status=200)

        return JsonResponse({'message':'NO_CONTENT'},status=404)

class CommentView(View):
    def post(self,request):
        try:
            comment_data = json.loads(request.body)

            if not User.objects.filter(id=comment_data['user_id']).exists():
                return JsonResponse({'message':'NO_VALIDATION_USER'},status=401)

            Comment.objects.create(
                user_id = comment_data['user_id'],
                post_id = comment_data['post_id'],
                comment = comment_data['comment']
            )

            return JsonResponse({'message':'ADDED_COMMENT'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

    def get(self,request):
        comment_data = json.loads(request.body)
        post_comments = Comment.objects.filter(post_id=comment_data['post_id'])

        if post_comments:
            comments = []

            for a_comment in post_comments:
                comments.append({
                    'comment':a_comment.comment
                })

            return JsonResponse({'result':comments},status=200)

        return JsonResponse({'message':'NO_COMMENT'},status=400)







