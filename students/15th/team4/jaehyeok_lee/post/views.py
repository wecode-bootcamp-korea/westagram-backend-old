from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder

from post.models import Post, Comment
from user.models import User


# Create your views here.
class Upload(View):
    def post(self, request):
        data = json.loads(request.body)
        
        data_writer = User.objects.get(account = data['writer'])
        data_img_url = data['img']
        data_content = data['content']

        Post.objects.create(writer = data_writer, img_url = data_img_url, content = data_content)
        return JsonResponse({"message": "SUCCESS"}, status = 200)


class Load(View):
    def get(self, request):
        posts = Post.objects.all()
        user_get = User.objects.get
        results = []
        for post in posts:
            results.append(
                {
                    "writer":  user_view(id=post.writer_id).account,
                    "content": post.content,
                    "datetime": post.date,
                    "img": post.img_url,
                }
            )
        return JsonResponse({"result": results}, status = 200)


class WriteComment(View):
    def post(self, request):
        data = json.loads(request.body)

        data_post = Post.objects.get(id = data['post_id'])
        data_writer = User.objects.get(account = data['writer'])
        data_content = data['content']

        Comment.objects.create(post = data_post, writer = data_writer, content = data_content)
        return JsonResponse({"message": "SUCCESS"}, status = 200)


class ReadComment(View):
    def get(self, request):
        data = json.loads(request.body)
        comments = Comment.objects.filter(post_id = data['post_id'])
        
        results= []
        for comment in comments:
            results.append(
                {
                    "writer": User.objects.get(id = comment.writer_id).account,
                    "content": comment.content,
                    "datetime": comment.datetime,
                }
            ) 
        return JsonResponse({"results": results}, status = 200)
