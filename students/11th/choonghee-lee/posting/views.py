import json

from django.core          import serializers
from django.http          import JsonResponse
from django.views.generic import View

from account.models import User
from .models        import Post, Comment

class PostView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']
            text    = data['text']
            img_url = data['img_url']

            user = User.objects.get(id=user_id)
            Post(
                user    = user,
                text    = text,
                img_url = img_url,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER_ID'}, status = 400)

    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = serializers.serialize('json', posts)
        return JsonResponse(serialized_posts, safe = False)

class CommentView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']
            post_id = data['post_id']
            text    = data['text']

            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)
            Comment(
                user = user,
                post = post,
                text = text,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER_ID'}, status = 400)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST_ID'}, status = 400)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id = post_id)
            comments = Comment.objects.filter(post__id__contains = post_id)
            serialized_comments = serializers.serialize('json', comments)
            return JsonResponse(serialized_comments, safe = False)
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST_ID'}, status = 400)