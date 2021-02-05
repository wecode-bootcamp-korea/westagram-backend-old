import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError
from django.db.models import Q

from posting.models   import Post, Comment, PostLike
from user.models      import User
from westagram.utils  import login_decorator


class PostView(View):
    @login_decorator
    def post(self, request, data, user):
        try:
            image_url = data['image_url']
            Post.objects.create(user=user, image_url=image_url)
            return JsonResponse({'message':'SUCCESS'}, status=200)
            
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
    @login_decorator
    def post(self, request, data, user):
        try:
            post_id = data['post_id']
            comment_body = data['comment_body']
            
            if Post.objects.filter(id=post_id).exists():
                post = Post.objects.get(id=post_id)
                Comment.objects.create(post=post, user=user, comment_body=comment_body)
                return JsonResponse({'message':'SUCCESS'}, status=200)
        
            return JsonResponse({'message':'INVALID_POST'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

class CommentShowView(View):
    def get(self, request):
        comments = Comment.objects.all()
        if not len(comments):
            return JsonResponse({'message':'NO_COMMENTS'}, status=200)
        
        results  = []
        
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
        

class PostLikeView(View):
    @login_decorator
    def post(self, request, data, user):
        try:
            post_id = data['post_id']
                
            if Post.objects.filter(id=post_id).exists():
                post = Post.objects.get(id=post_id)
                postlike = PostLike.objects.update_or_create(post=post, user=user)[0]
                
                if postlike.like:
                    postlike.delete()
                else:
                    postlike.like = True
                    postlike.save()

                post.like = len(list(PostLike.objects.filter(post=post_id, like=True)))
                post.save()
                return JsonResponse({'message':'SUCCESS'}, status=200)
                    
            return JsonResponse({'message':'INVALID_POST'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)