import json

from django.views import View
from django.http  import JsonResponse
from django.core  import exceptions

from account.models import User
from .models        import Post, Comment, Like
from core.utils     import login_decorator



class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not data.get('img_url'):
                return JsonResponse({'message': 'TYPE IMG_URL'}, status=400)
            
            if not data.get('content'):
                return JsonResponse({'message': 'TYPE CONTENT'}, status=400)

            user_id = request.user.id

            Post.objects.create(
                image_url    = data['img_url'],
                content      = data['content'],
                user_id      = user_id
            )
            
            return JsonResponse({'message': 'SUCCSESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
    def get(self, request):
        posts  = Post.objects.all()
        result = []
        
        for post in posts:
            user_name = post.user.user_name
            
            post_dict = {
                'user_name'  : user_name,
                'image_url'  : post.image_url,
                'content'    : post.content,
                'create_date': post.create_date,
            }
            result.append(post_dict)

        return JsonResponse({'result': result}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not data.get('content'):
                return JsonResponse({'message': 'TYPE CONTENT'}, status=400)
            
            if not data.get('post_id'):
                return JsonResponse({'message': 'TYPE POST_ID'}, status=400)

            user_id = request.user.id
            post_id = Post.objects.get(id=data['post_id']).id

            Comment.objects.create(
                content = data.get('content'),
                post_id = post_id,
                user_id = user_id,
            )

            return JsonResponse({'result': 'SUCCSESS'}, status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID POST'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        
    def get(self, request):
        try :
            data = json.loads(request.body)
            
            if not data.get('post_id'):
                return JsonResponse({'message': 'TYPE POST_ID'}, status=400)
            
            post_id  = Post.objects.get(id=data['post_id']).id
            comments = Comment.objects.filter(post=post_id)

            if not comments:
                return JsonResponse({'massage': 'No Comments'}, status=200)
            
            result = []

            for comment in comments:
                comment_dict = {
                    'user_name'  : comment.user.user_name,
                    'content'    : comment.content,
                    'create_date': comment.create_date,
                }
                result.append(comment_dict)

            return JsonResponse({'result': result}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID POST'}, status=400)

class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id = request.user.id
            post = Post.objects.get(id=data['post_id'])

            Like.objects.create(
                user_id = user_id,
                post_id = post.id
            )

            post.likes += 1
            post.save()
            
            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST'}, status=400)

class DeletePostView(View):
    @login_decorator
    def delete(self,request):
        try:
            data = json.loads(request.body)

            user_id = request.user.id
            post_id = data.get('post_id')

            post = Post.objects.get(id=post_id)
            
            if post.user_id != user_id:
                return JsonResponse({'message': 'Unauthorized'}, status=400)
            
            post.delete()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except Post.DoesNotExist:
            return JsonResponse({'message': 'INVALID_POST'}, status=400)
