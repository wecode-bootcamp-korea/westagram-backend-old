import json

from django.views import View
from django.http  import JsonResponse, request

from .models      import ThumbsUp
from user.models  import User
from post.models  import Posting
from user.utils   import login_decorator


class ThumbsUpView(View):
    @login_decorator
    def post(self,  request):
        data = json.loads(request.body)
        user = User.objects.get(id = request.user)
        post = Posting.objects.get(id = data['post_id'])
        
        try:  
            if ThumbsUp.objects.filter(post = data['post_id']):
                return JsonResponse({'message' : 'OVERLAP_ERROR'},status = 400)
            
            ThumbsUp(user = user, post = post).save()

            return JsonResponse({'message' : "SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERORR'}, status=400)

    def get(self, request):
        data = json.loads(request.body)
        try:
            likes = ThumbsUp.objects.filter(post= data['post_id'])
            like_nums=len(likes)
        
            likes ={
                'content'     : likes[0].post.content,
                'description' : likes[0].post.description,
                'created_at'  : str(likes[0].post.created_at),
                'author'      : likes[0].post.author,
                'thumbs_up'   : like_nums
            }

            return JsonResponse({'result' : likes})
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class DeleteLikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            ThumbsUp.objects.get(post=data['post_id'], user=request.user).delete()
            return JsonResponse({'message' : "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
        except ThumbsUp.DoesNotExist:
            return JsonResponse({"message" : 'NOT_EXIST'}, status=400)
