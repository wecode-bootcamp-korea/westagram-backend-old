import json

from django.views     import View
from django.http      import JsonResponse

from .models     import Post, Comment, Like
from user.models import User
from core.utils  import login_decorator

class PostView(View):
    def get(self, request):
            posts    = Post.objects.select_related('author').prefetch_related('comment_set', 'like_set')
            context  = [
                {
                    'id'       : post.id,
                    'author'   : post.author.username,
                    'title'    : post.title,
                    'image'    : post.image_url,
                    'created'  : post.created_at,
                    'likes'    : post.like_set.count(),
                    'comments' : [
                        {
                            'parent'  : cmt.parent_id,
                            'created' : cmt.created_at,
                            'content' : cmt.content,
                            'id': cmt.id
                        }
                        for cmt in post.comment_set.all()
                    ]
                }
                for post in posts
            ]
            return JsonResponse({'result':context}, status = 200)

    @login_decorator
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            Post.objects.create(
                author    = user,
                title     = data['title'],
                image_url = data['image_url'],
                content   = data.get('content', None)
            )


#            data = json.loads(request.body)
#            post = Post()
#            post.author =  User.objects.get(id = data['user_id'])
#            post.title = data['title']
#            post.image_url = data['image_url']
#            if 'content' in data:
#                post.content= data['content']
#            post.save()
            return JsonResponse({'message': 'POST HAS BEEN CREATED SUCCESSFULLY!'}, status = 201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decorator
    def put(self, request):
        try:
            data = json.loads(request.body)
            obj  = Post.objects.get(id=data['id'])
            if 'title' in data:
                obj.title = data['title']
            if 'content' in data:
                obj.content = data['content']
            if 'image' in data:
                obj.image = data['image']
            obj.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            if Post.objects.filter(id = data['id']).exists():
               q = Post.objects.get(id = data['id'])
               q.delete()
               return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


class CommentView(View):

    def get(self, request):
        try:
            data = json.loads(request.body)
            comments = Comment.objects.filter(post_id = data['post_id']).prefetch_related('author')
            context = [
                {
                    'feed_id'      : cmt.post_id.id,
                    'author'       : cmt.author.username,
                    'content'      : cmt.content,
                    'created_time' : cmt.comment_created,
                    'parent'       : cmt.parent_id
                }
                for cmt in comments
            ]

            return JsonResponse({'result':context}, status = 200)
        except KeyError:
            JsonResponse({'message':'nope'}, status = 400)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            Comment.objects.create(
                author  = User.objects.get(id = data['user_id']),
                post_id = Post.objects.get(id = data['post_id']),
                content = data['content'],
                parent  = data.get('parent_id', None)
            )
            return JsonResponse({'meesage':'SUCCESS'}, status = 200)
        except KeyError:
            JsonResponse({'message':'KEY_ERROR'}, status = 400)

    @login_decorator
    def put(self, request):
        try:
            data = json.loads(request.body)
            if Comment.objects.filter(id=data['id']).exists():
                q = Comment.objects.get(id=data['id'])
                q.content = data['content']
                q.save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'meesage':'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            if Comment.objects.filter(id=data['id']).exists():
                q = Comment.objects.get(id=data['id'])
                q.delete()
                return JsonResponse({'message':'cmt, success'}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 200)

#class LikeView(View):
#
#    def post(self, request):
#        try:
#            data=json.loads(request.body)
#            Like.objects.create(user_id = data['user_id'], post_id = data['post_id'], status = True)
#            return JsonResponse({'message':'SUCCESS'}, status = 200)
#        except KeyError:
#            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
#    def delete(self, request):
#        try:
#            data = json.loads(request.body)
#            Like.objects.filter(user_id = data['user_id'], post_id = data['post_id']).delete()
#            return JsonResponse({'message':'SUCCESS'}, status = 200)
#        except KeyError:
#            return JsonResponse({'meesage':'KEY_ERROR'}, status = 400)
#class FollowView(View):
#    def post(self, request):
#        try:
#            data=json.loads(request.body)
#            Like.objects.create(user_id = data['user_id'], post_id = data['post_id'], stats = True)
#            return JsonResponse({'message':'SUCCESS'}, status = 200)
#        except KeyError:
#            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
#    def delete(self, request):
#        try:
#            data = json.loads(request.body)
#            Like.objects.filter(follower_id = data['follower_id'], followee_id = data['followee_id'])
#            return JsonResponse({'message':'SUCCESS'}, status = 200)
#        except KeyError:
#            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
