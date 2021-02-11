import json

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models     import Post, Comment
from user.models import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id=data['user_id']).exists():
                user = User.objects.get(id=data['user_id'])
                Post(
                    user    = user,
                    content = data['content']
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
            else:
                return JsonResponse({'message':'The user does not exist.'}, status = 401)
        except Exception as e:
            return JsonResponse({'message':f'{e}'}, status = 401)

    def get(self, request):
        db = Post.objects.values()
        return JsonResponse({'data':list(db)}, status = 200)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id=data['user_id']).exists() and Post.objects.filter(id=data['post_id']).exists():
                user = User.objects.get(id=data['user_id'])
                post = Post.objects.get(id=data['post_id'])
                Comment(
                    user = user,
                    post = post,
                    comment = data['comment']
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
            elif not User.objects.filter(id=data['user_id']).exists():
                return JsonResponse({'message':'The User does not exist.'}, status = 401)
            else:
                return JsonResponse({'message':'The Post does not exist.'}, status = 401)
        except  Exception as e:
            return JsonResponse({'message':f'{e}'}, status = 401)

    def get(self, request):
        db = Comment.objects.values()
        return JsonResponse({'data':list(db)}, status = 200)
