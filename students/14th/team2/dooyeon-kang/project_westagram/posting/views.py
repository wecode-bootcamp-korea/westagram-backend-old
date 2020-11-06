import json

from django.http import JsonResponse, QueryDict
from django.views import View
from django.db.models import Q

from posting.models import Posting, Comment
from user.models import User

class PostingView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            input_user  = data['user_id']
            image_url   = data['image_url']
            description = data['description']
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

        try:
            user = User.objects.get(id=input_user)
        except Exception:
            return JsonResponse({'message': 'INVALID USER'}, status = 401)

        try:
            Posting(
                image_url   = image_url,
                description = description,
                user        = user,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception:
            return JsonResponse({'message': 'Somthing wrong'}, status = 400)

    def get(self, request):
        posts = Posting.objects.values()

        try:
            result = [
                {'user': {
                    'user_id': post['user_id'],
                    'username': User.objects.get(id=post['user_id']).name
                 },
                 'comments': [comment for comment in Comment.objects.filter(posting_id=post['id']).values()],
                 'img_url': post['image_url'],
                 'description': post['description'],
                 'created_at': post['created_at']} for post in posts
            ]

            return JsonResponse({'result': result}, status = 200)

        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

class CommentView(View):

    def post(self, request):
        data = json.loads(request.body)

        try:
            input_user   = data['user_id']
            comment_text = data['text']
            posting_id   = data['posting_id']
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

        try:
            user_obj = User.objects.get(id=input_user)
        except Exception:
            return JsonResponse({'message': 'INVALID USER'}, status = 401)

        try:
            posting_obj = Posting.objects.get(id=posting_id)
        except Exception:
            return JsonResponse({'message': 'INVALID POSTING'}, status = 401)

        if not comment_text:
            return JsonResponse({'message': 'Cannot be none'}, status = 400)

        try:
            Comment(
                text    = comment_text,
                user    = user_obj,
                posting = posting_obj,
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except Exception as error_message:
            return JsonResponse({'meesage': error_message}, status = 401)

    def get(self, request):

        try:
            post_id = request.GET.get('post')
        except Exception as error_message:
            return JsonResponse({'message': error_message}, status = 400)

        try:
            comments = Comment.objects.filter(posting_id=post_id).values()
        except Exception:
            return JsonResponse({'message': 'No comment for this posting'}, status = 400)

        result = [
            {'posting_id': comment['posting_id'],
             'user': {
                'user_id': comment['user_id'],
                'username': User.objects.get(id=comment['user_id']).name
             },
             'text': comment['text'],
             'created_at': comment['created_at'] } for comment in comments
        ]

        try:
            return JsonResponse({'result': result}, status = 200)
        except Exception:
            return JsonResponse({'message': 'Something Wrong'}, status = 400)
