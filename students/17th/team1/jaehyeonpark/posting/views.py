import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError
from django.db.models import Q

from posting.models   import Post, Comment
from user.models      import User

class PostView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user_id      = data['user_id']
            image_url    = data['image_url']
                
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                Post.objects.create(user=user, image_url=image_url)
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

class PostShowView(View):
    def get(self, request):
        try:
            posts   = Post.objects.all()
            results = []
            
            for post in posts:
                results.append(
                    {
                    "account":post.user.account,
                    "image_url":post.image_url
                    }
                )

            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class CommentView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']
            post_id = data['post_id']
            comment_body = data['comment_body']
                
            if  {
                User.objects.filter(id=user_id).exists()
                and Post.objects.filter(id=post_id).exists()
                }:
                user = User.objects.get(id=user_id)
                post = Post.objects.get(id=post_id)

                Comment.objects.create(post=post, user=user, comment_body=comment_body)
                return JsonResponse({'message':'SUCCESS'}, status=200)
            
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

class CommentShowView(View):
    def get(self, request):
        try:
            comments   = Comment.objects.all()
            results = []
            
            for comment in comments:
                results.append(
                    {
                    "post":comment.post.id,
                    "user":comment.post.user.account,
                    "created_at":comment.created_at,
                    "comment_body":comment.comment_body
                    }
                )

            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
