import json
import jwt

from django.views import View
from django.http  import JsonResponse, HttpResponse

from . models     import Post, Comment, CommentReply, Like
from user.models  import User
from user.utils   import login_decorator


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            image_url = data['image_url']
            caption   = data['caption']
            user      = request.user.id

            Post.objects.create(
                    image_url = image_url,
                    caption   = caption,
                    user_id   = user
                    )
            
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def patch(self, request):
        try:
            data      = json.loads(request.body)
            image_url = data['image_url']
            caption   = data['caption']
            post_id   = data['post_id']
            user_id   = request.user.id

            if Post.objects.filter(id=post_id, user_id=user_id).exists():
                Post.objects.filter(id=post_id).update(
                        image_url = image_url,
                        caption   = caption
                        )

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            
            return JsonResponse({'message': 'CANNOT_UPDATE_POST'}, status=403)

        except KeyError:
            return JsonResponse({'message': 'Key_Error'}, status=400)

class PostDetailView(View):
    @login_decorator
    def get(self, request, post_id):
        try:
            post_user_id  = Post.objects.get(id=post_id).user_id
            post_username = User.objects.get(id=post_user_id).username
            post_image    = Post.objects.get(id=post_id).image_url
            total_likes   = len(Post.objects.get(id=post_id).like.all())
            caption       = Post.objects.get(id=post_id).caption
            top_comments  = Post.objects.get(id=post_id).comment.all()[:5]
            top_comments  = [{
                'date_time': comment.date_time,
                'text'     : comment.text,
                'user_id'  : comment.user_id
                } for comment in top_comments]

            return JsonResponse({'data': {
                'post_username': post_username,
                'post_image'   : post_image,
                'total_likes'  : total_likes,
                'caption'      : caption,
                'top_comments' : top_comments
                }}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST'}, status=400)
        

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            text    = data['text']
            post_id = data['post_id']
            user_id = request.user.id

            Comment.objects.create(
                    text    = text,
                    user_id = user_id,
                    post_id = post_id
                    )

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class CommentDetailView(View):
    @login_decorator
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)

            if post.comment.all():
                comments_list = [{
                    'date_time': comment.date_time,
                    'text'     : comment.text,
                    'user_id'  : comment.user_id,
                    } for comment in post.comment.all()]

                return JsonResponse({'data':comments_list}, status=200)
            
            else:
                return JsonResponse({'message':'NO_COMMENTS'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message':'INVALID_POST'}, status=400)

    @login_decorator
    def delete(self, request, post_id):
        try:
            data       = json.loads(request.body)
            comment_id = data['comment_id']
            user_id    = request.user.id

            if Comment.objects.filter(id=comment_id, user_id=user_id, post_id=post_id).exists():
                Comment.objects.get(id=comment_id).delete()

                return JsonResponse({'message': "SUCCESS"}, status=200)

            return JsonResponse({'message': 'CANNOT_DELETE_COMMENT'}, status=403)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class CommentReplyView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            comment_id = data['comment_id']
            text       = data['text']
            user_id    = request.user.id

            if Comment.objects.filter(id=comment_id).exists():
                CommentReply.objects.create(text=text, comment_id=comment_id, user_id=user_id)

                return JsonResponse({'message': 'SUCCESS'}, status=201)

            return JsonResponse({'message': 'INVALID_COMMENT'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            post_id = data['post_id']
            user_id = request.user.id

            if Like.objects.filter(post_id=post_id, user_id=user_id).exists():
                Like.objects.filter(post_id=post_id, user_id=user_id).delete()

                return JsonResponse({'message':'SUCCESS'}, status=200)

            else:
                Like.objects.create(
                        user_id = user_id,
                        post_id = post_id
                        )

                return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LikeDetailView(View):
    @login_decorator
    def get(self, request, post_id):
        try:
            liked_users      = Post.objects.get(id=post_id).like.all()
            liked_users_list = [{
                'username'  : User.objects.get(id=user.user_id).username,
                'full_name' : User.objects.get(id=user.user_id).full_name
                } for user in liked_users]

            return JsonResponse({'data': liked_users_list}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST'}, status=400)
            







