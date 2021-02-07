import json
import jwt

from django.views import View
from django.http  import JsonResponse, HttpResponse

from . models     import Post, Comment
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















