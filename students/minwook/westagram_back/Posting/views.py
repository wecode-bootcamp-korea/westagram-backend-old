import json

from django.views import View
from django.http  import JsonResponse

from .models     import Posting, Comment
from User.models import User

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user  = data['user']
            image = data['image']
            text  = data['text']

            user_id = 0
            if '@' in user and '.' in user:
                user_id = User.objects.get(email = user)
            elif user.isdigit():
                user_id = User.objects.get(phone = user)
            elif user.isalpha():
                user_id = User.objects.get(name = user)

            Posting(
                user  = user_id,
                image = image,
                text  = text
            ).save()
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        return JsonResponse({'message':'SUCCESS'}, status = 200)

    def get(self, request):
        post_data = Posting.objects.values()
        return JsonResponse({'message':list(post_data)}, status = 200)

class CommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            post = data['post']
            user = data['user']
            text = data['text']

            post_id = Posting.objects.get(id = post)
            user_id = User.objects.get(name = user)

            Comment(
                post = post_id,
                user = user_id,
                text = text
            ).save()
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER_OR_POST_ID'}, status = 400)
        return JsonResponse({'message':'SUCCESS'}, status = 200)

    def get(self, request):
        comment_data = Comment.objects.values()
        return JsonResponse({'message':list(comment_data)}, status = 200)
