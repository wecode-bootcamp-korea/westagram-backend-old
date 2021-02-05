import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError
from django.db.models import Q

from posting.models   import Post, Comment, PostLike, Follow
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

class FollowView(View):
    @login_decorator
    def post(self, request, data, user):
        try:
            to_user = data['to_user']

            if User.objects.filter(id=to_user).exists():
                follow_user = User.objects.get(id=to_user)

                if user == follow_user:
                    return JsonResponse({'message':'CANNOT_FOLLOW_SELF'}, status=200)

                if Follow.objects.filter(from_user=user, to_user=follow_user).exists():
                    Follow.objects.get(from_user=user, to_user=follow_user).delete()
                else:
                    Follow.objects.create(from_user=user, to_user=follow_user)

                return JsonResponse({'message':'SUCCESS'}, status=200)
                    
            return JsonResponse({'message':'INVALID_FOLLOW_USER'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class CommentDeleteView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data['comment_id']

            if Comment.objects.filter(id=comment_id).exists():
                comment = Comment.objects.get(id=comment_id)
                comment.delete()
                return JsonResponse({'message':'SUCCESS'}, status=200)
        
            return JsonResponse({'message':'INVALID_COMMENT'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

