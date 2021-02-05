import json
import bcrypt

from django.http  import JsonResponse
from django.views import View

from user.models import User
from posting.models import Post, Comment

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            account = data.get('account')
            password = data.get('password')
            title = data.get('title')
            image_url = data.get('image_url')

            if not User.objects.filter(account=account).exists():
                return JsonResponse({'MESSAGE': 'CHECK_ACCOUNT'}, status=409)
            id = User.objects.get(account=account)

            if bcrypt.checkpw(password.encode('utf-8'), (id.password).encode('utf-8')) == False:
                return JsonResponse({'MESSAGE': 'CHECK_PASSWORD'}, ststus=409)
            Post.objects.create(title=title, image=image_url, user_id=id.id)
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    def get(self, request):
        try:
            data = json.loads(request.body)
            account = data['account']
            results = []
            posts = Post.objects.filter(user_id=User.objects.get(account=account).id)
            for post in posts:
                results.append(
                        {"account":account,
                        "image_url":post.image,
                        "title":post.title,
                        "created_at":post.created_at,}
                        )
            return JsonResponse({"RESULT": results}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=400)

class CommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Comment.objects.create(
                    post_id=Post.objects.get(title=data['title']).id,
                    content=data['content']
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

    def get(self, request):
        data = json.loads(request.body)
        results = []
        comments = Comment.objects.filter(post_id=Post.objects.get(title=data['title']))
        for comment in comments:
            results.append({
                "post":comment.post.title,
                "content":comment.content,
                "created_at":comment.created_at,
                })
        return JsonResponse({'RESULT': results}, status=200)
