import json

from django.views import View
from django.http  import JsonResponse, request

from .models      import Follow
from user.models  import User
from user.utils   import login_decorator

class FollowingView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        followed = User.objects.get(id = data['user_id'])
        follower = User.objects.get(id = request.user)
        try:
            if Follow.objects.filter(be_followed = data['user_id']):
                return JsonResponse({'message' : 'OVELAP_ERROR'},status=400)
            
            Follow.objects.create(be_followed = followed, follower = follower)

            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    
    @login_decorator
    def get(self, request):
        data = json.loads(request.body)
        try:
            follows = Follow.objects.filter(be_followed = data['user_id'])
            follow_nums = len(follows)
            print(follows[0])
            print(follows[0].be_followed.name)
            follows = {
                'user_name' : follows[0].be_followed.name,
                'follower'  : follow_nums
            }

            return JsonResponse({'result' : follows}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class DeleteFollowView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        try:
            Follow.objects.get(be_followed=data['user_id'], follower=request.user).delete()
            return JsonResponse({'message' : 'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'},status=400)
        
        except Follow.DoesNotExist:
            return JsonResponse({'message' : 'NOT_EXIST'},status=400)

