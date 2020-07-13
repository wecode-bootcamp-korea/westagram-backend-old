import json

from django.http    import JsonResponse
from django.views   import View

from users.models   import User,Following

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['name'] and data['email'] and data['password']:

                if '@' not in data['email']:
                    return JsonResponse({'message':'Invalid email format'}, status=401)

                if User.objects.filter(email=data['email']).exists():
                    return JsonResponse({'message':'Already registered User_ID'}, status=401)

                if len(data['password']) < 5:
                    return JsonResponse({'message':'Password must be at least 5 chracters.'}, status=401)

                User(
                    name        = data['name'],
                    email       = data['email'],
                    password    = data['password']
                ).save()                
                return JsonResponse({'message':'Register Success'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)

        if User.objects.filter(email=data['email']).exists():  
            login_user = User.objects.get(email=data['email'])

            if login_user.password == data['password']:
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'INVALID ID or PASSWORD'}, status=401)

        return JsonResponse({'message':'INVALID ID or PASSWORD'}, status=401)

class FollowUserView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(id=data['followed_user_id']).exists() and User.objects.filter(id=data['following_user_id']).exists():
                following_users = list(Following.objects.filter(followed_user=data['followed_user_id']).values('following_user_id'))

                for following_user in following_users:
                    if int(data['following_user_id']) == following_user['following_user_id']:
                        return JsonResponse({'message':'Already Followed'}, status=401)
                    
                Following(
                        followed_user_id     =   data['followed_user_id'],
                        following_user_id    =   data['following_user_id']
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
