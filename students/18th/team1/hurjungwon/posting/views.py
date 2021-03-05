import json

from django.views import View
from django.http  import JsonResponse
from django.core  import exceptions

from account.models import User
from .models        import Post, Comment


class PostView(View):
    def post(self, request):
        
        if not request.body:
            return JsonResponse({'message': 'Empty Value'}, status=400)
        
        data = json.loads(request.body)

        try:
            user_name = User.objects.get(user_name=data['user_name'])
            user_id   = user_name.id

            Post.objects.create(
                image_url    = data['img_url'],
                content      = data['content'],
                user_name_id = user_id
            )
            
            return JsonResponse({'message': 'SUCCSESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
    def get(self, request):
        posts = Post.objects.all()
        
        result = []
        
        for post in posts:
            user_id   = post.user_name
            user_name = user_id.user_name
            
            post_dict = {
                'user_name'  : user_name,
                'image_url'  : post.image_url,
                'content'    : post.content,
                'create_date': post.create_date,
            }
            result.append(post_dict)

        return JsonResponse({'result': result}, status=200)

class CommentView(View):
    def post(self, request):
        
        if not request.body:
            return JsonResponse({'message': 'Empty Value'}, status=400)
        
        data = json.loads(request.body)

        try:
            post_id   = data['post_id']
            user_name = User.objects.get(user_name=data['user_name']).id
            
            if not Post.objects.filter(id=post_id):
                return JsonResponse({'massage': 'Invalid Post_ID'}, status=400)
                
            Comment.objects.create(
                content      = data['content'],
                post_id      = data['post_id'],
                user_name_id = user_name,
            )

            return JsonResponse({'result': 'SUCCSESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status=400)
            
    def get(self, request):

        if not request.body:
            return JsonResponse({'message': 'Type Post_ID'}, status=400)
        
        data = json.loads(request.body)

        try :
            post_id = data['post_id']
            
            if not Post.objects.filter(id=post_id):
                return JsonResponse({'massage': 'Invalid Post_ID'}, status=400)

            comments = Comment.objects.filter(post=post_id)
            
            if not comments:
                return JsonResponse({'massage': 'No Comments'}, status=200)
            
            result = []

            for comment in comments:
                comment_dict = {
                    'user_name'  : comment.user_name.user_name,
                    'content'    : comment.content,
                    'create_date': comment.create_date,
                }
                result.append(comment_dict)

            return JsonResponse({'result': result}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
