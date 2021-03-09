import json
from json.decoder import JSONDecodeError

from django.views import View
from django.http  import JsonResponse, request

from user.models    import User
from posting.models import Post, Comment

class PostUploadView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user    = data['user']
            content = data['content']
            img_url = data['img_url']

            user = User.objects.get(email=user)

            if Post.objects.filter(user=user, img_url=img_url):
                return JsonResponse({'message':'IMAGE ALREADY EXISTS'}, status=400)

            Post.objects.create(
                user    = user,
                content = content,
                img_url = img_url                
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except Exception as e:
            print(e)

    def get(self, request):
        posts   = Post.objects.all()
        results = []

        for post in posts:
            results.append(
                {
                    'user'       : post.user.email,
                    'content'    : post.content,
                    'img_url'    : post.img_url,
                    'create_date': post.create_date
                }
            )

        return JsonResponse({'results':results}, status=200)

class CommentUploadView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = data['user']
            post = data['post']
            content = data.get('content', None)

            user_id = User.objects.get(id=user)
            post_id = Post.objects.get(id=post)

            Comment.objects.create(
                user    = user_id,
                post    = post_id,
                content = content
            )
            
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'message':'INVALID_POST'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except Exception as e:
            print(e)
    
    def get(self, request):
        comments   = Comment.objects.filter(post_id=1)
        results = []

        for comment in comments:
            results.append(
                {
                    'content'     : comment.content,
                    'create_date' : comment.create_time,
                    'email'       : comment.user.email,
                    'phone'       : comment.user.phone,
                    'full_name'   : comment.user.full_name,
                    'user_name'   : comment.user.user_name    
                }
            )

        return JsonResponse({'results':results}, status=200)