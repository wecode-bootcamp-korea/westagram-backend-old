import json
import jwt
import my_settings
from utils import login_decorator

from json.decoder import JSONDecodeError
from jwt import InvalidSignatureError
from posting.models import Comment
from posting.models import Posting
from posting.models import UserPostingLike
from user.models import User

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


SECRET_KEY = my_settings.SECRET_KEY['secret']


class PostingView(View):
    @login_decorator
    def post(self, request):

        try:
            data = json.loads(request.body)
            user = request.user

            title = data.get('title', None)
            content = data.get('content', None)
            image_url = data.get('image_url', None)
            ACCESS_TOKEN = data.get('ACCESS_TOKEN', None)
            # print("'"+ACCESS_TOKEN+"'")
            # ACCESS_TOKEN = ACCESS_TOKEN.encode('utf-8')

            if not (title and content and image_url and ACCESS_TOKEN):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # payload = jwt.decode(ACCESS_TOKEN, SECRET_KEY, algorithms='HS256')
            # print(payload)
            # user = User.objects.get(id=payload['user_id'])
            # if not user:
            #     return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)

            Posting.objects.create(
                user_id=user.id,
                title=title,
                content=content,
                image_url=image_url,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except InvalidSignatureError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=401)

    def get(self, request):

        postings = Posting.objects.all()

        result = []
        for posting in postings:
            posting_info={
                'user_name': posting.user.name,
                'title': posting.title,
                'content': posting.content,
                'image': posting.image_url,
            }
            result.append(posting_info)

        return JsonResponse({'message': 'SUCCESS', 'posting': result}, status=200)


class CommentView(View):
    @login_decorator
    def post(self, request):

        try:
            data = json.loads(request.body)
            user = request.user

            content = data.get('content', None)

            # 일단 request.body로 받고
            # 구헌하고 url로 받는 것으로 구현해보자
            posting_id = data.get('posting_id', None)

            if not (content and posting_id):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            comment = Comment.objects.create(
                content=content,
                posting_id=posting_id,
                user_id=user.id,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

    def get(self, request):

        comments = Comment.objects.all()

        result = []
        for comment in comments:
            comment_info = {
                'comment': comment.content,
                'posting_id': comment.posting_id,
                'posting_title': comment.posting.title,
                'user_email': comment.user.email,
                'create_date': comment.create_date,
            }

            result.append(comment_info)

        return JsonResponse({'message': 'SUCCESS', 'comment': result}, status=200)


class CommentDetailView(View):
    def get(self, request, posting_id):

        comments = Comment.objects.filter(posting_id=posting_id)

        result = []
        for comment in comments:
            comment_info = {
                'comment': comment.content,
                'posting_id': comment.posting_id,
                'posting_title': comment.posting.title,
                'user_email': comment.user.email,
                'create_date': comment.create_date,
            }

            result.append(comment_info)

        return JsonResponse({'message': 'SUCCESS', 'comment': result}, status=200)


class LikeView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            posting = Posting.objects.get(id=posting_id)
            user = request.user

            if UserPostingLike.objects.filter(user_id=user.id, posting_id=posting_id).exists():
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

            like = posting.like.add(user)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POSTING'}, status=400)


class UnlikeView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            posting = Posting.objects.get(id=posting_id)
            user = request.user

            if not UserPostingLike.objects.filter(user_id=user.id, posting_id=posting_id).exists():
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=400)

            unlike = UserPostingLike.objects.get(user_id=user.id, posting_id=posting_id).delete()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POSTING'}, status=400)


class PostingDeleteView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            user = request.user
            posting = Posting.objects.get(id=posting_id)

            if posting.user_id != user.id:
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=401)

            posting.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POSTING'},status=400)


class CommentDeleteView(View):
    @login_decorator
    def post(self, request, comment_id):
        try:
            user = request.user
            comment = Comment.objects.get(id=comment_id)

            if not comment.user_id == user.id:
                return JsonResponse({'message': 'INVALID_REQUEST'}, status=401)

            comment.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Comment.DoesNotExist:
            return JsonResponse({'mssage': 'INVALID_COMMENT'}, status=400)



"""

    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    image_url = models.URLField(null=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    like = models.ManyToManyField('u
    """
class PostingUpdateView(View):
    @login_decorator
    def post(self, request, posting_id):
        try:
            data = json.loads(request.body)
            user = request.user
            posting = Posting.objects.get(id=posting_id)

            title = data.get('title', None)
            content = data.get('content', None)
            image_url = data.get('image_url', None)

            if posting.user_id != user.id:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            posting.title = title
            posting.content = content
            posting.image_url = image_url
            posting.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POSTING'}, status=400)

