import json

from django.views   import View 
from django.http    import JsonResponse

from .models import (
    User,
    Follow
)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'message':'EXISTING_ACCOUNT'}, status=401)
            if ('@' in data['email']) and (len(data['password'])>=5) : 
                User(
                    name        = data['name'],
                    email       = data['email'],
                    password    = data['password']
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status=200)
            return JsonResponse({'message' : 'VALIDATION_ERROR'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(name=data['user']).exists():
                user = User.objects.get(name=data['user'])
            elif User.objects.filter(email=data['user']).exists():
                user = User.objects.get(email=data['user'])
        
            if user.password == data['password']:
                return JsonResponse({'message' : 'SUCCESS'}, status=200)
            return JsonResponse({"message":'UNAUTHORIZED'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class FollowView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if (User.objects.filter(id=data['from_user']).exists()) and (User.objects.filter(id=data['to_user']).exists()):
                if Follow.objects.filter(from_user = data['from_user'], to_user = data['to_user']).exists():
                    follow = Follow.objects.get(from_user = data['from_user'], to_user = data['to_user'])
                    follow.status = 'follow'
                    follow.save()
                    return JsonResponse({'message' : 'FOLLOW SUCCESS'}, status=200)
                Follow(
                        from_user   = User.objects.get(id=data['from_user']),
                        to_user     = User.objects.get(id=data['to_user']),
                        status      = 'follow'
                ).save()
                return JsonResponse({'message' : 'FOLLOW SUCCESS'}, status=200)
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class UnFollowView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if (User.objects.filter(id=data['from_user']).exists()) and (User.objects.filter(id=data['to_user']).exists()):
                if Follow.objects.filter(from_user = data['from_user'], to_user = data['to_user']).exists():
                    follow = Follow.objects.get(from_user = data['from_user'], to_user = data['to_user'])
                    follow.status = 'unfollow'
                    follow.save()
                    return JsonResponse({'message' : 'UNFOLLOW SUCCESS'}, status=200)
                return JsonResponse({'message' : 'NOT ALLOWED'}, status=401)
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
