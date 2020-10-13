import json

from django.http import JsonResponse
from django.views import View
from posting.models import Posting, Comment, Like, Reply
from user.models import User

# Create your views here.

class UploadView(View):

    def post(self, request):
        data = json.loads(request.body)
        Posting(
            user = User.objects.get(id=data['user']),
            img = data['img'],
            description = data['description'],
            upload_time = data['upload_time']
        ).save()

        return JsonResponse(
            {'MESSAGE': 'UPLOAD_SUCCESS'},
            status=201)

class ShowView(View):

    def get(self, request):
        all_posts = Posting.objects.all().values()
        post_list = []
        for post in all_posts:
            post_list.append(post)

        return JsonResponse(
            {'MESSAGE':post_list},
            status = 200
        )

class DeleteView(View):

    def delete(self, request):
        data = json.loads(request.body)
        Posting.objects.get(id=data['target']).delete()
        return JsonResponse(
            {'MESSAGE': 'DELETED'},
            status=200)


class UpdateView(View):

    def post(self, request):
        data = json.loads(request.body)
        target = Posting.objects.get(id=data['target'])
        target.description = data['description']
        target.save()
        return JsonResponse(
            {'MESSAGE': 'UPDATED'},
            status=200)
        

class UploadCommentView(View):

    def post(self, request):
        data = json.loads(request.body)
        Comment(
            user = User.objects.get(id=data['user']),
            post = Posting.objects.get(id=data['post']),
            upload_time = data['upload_time'],
            content = data['content']
        ).save()
        return JsonResponse(
            {'MESSAGE': 'UPLOAD_SUCCESS'},
            status=201)

class ReplyView(View):

    def post(self, request):
        data = json.loads(request.body)
        Reply(
            user = User.objects.get(id=data['user']),
            comment = Comment.objects.get(id=data['comment']),
            upload_time = data['upload_time'],
            content = data['content']
        ).save()
        return JsonResponse(
            {'MESSAGE': 'UPLOAD_SUCCESS'},
            status=201)


class ShowCommentView(View):

    def get(self, request):
        data = json.loads(request.body)
        comments = Comment.objects.filter(post_id = data['post']).values()
        comment_list = []
        for com in comments:
            comment_list.append(com)
        return JsonResponse(
            {'MESSAGE': comment_list},
            status = 200
        )

class DeleteCommentView(View):

    def delete(self, request):
        data = json.loads(request.body)
        Comment.objects.get(id=data['target']).delete()
        return JsonResponse(
            {'MESSAGE': 'DELETED'},
            status=200)



class LikeView(View):

    def post(self, request):
        data = json.loads(request.body)
        Like(
            post = Posting.objects.get(id=data['post']),
            user = User.objects.get(id=data['user'])
        ).save()
        return JsonResponse(
            {'MESSAGE':'SUCCESS'},
            status=201
        )
