import json

from django.views           import View
from django.http            import JsonResponse 

from user.models  import User

class SignUpView(View):
    def post(self, request):
        signup_data = json.loads(request.body)

        try:
            if '@' not in signup_data['email'] or '.' not in signup_data['email']:
              return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if User.objects.filter(email=signup_data['email']).exists() or User.objects.filter(phone=signup_data['phone']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)
            
            if User.objects.filter(nickname=signup_data['nickname']).exists():
                return JsonResponse({'message':'NICKNAME_ALREADY_EXISTS'}, status=409)

            if len(signup_data['password']) < 8:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=400)

            User.objects.create(
                email    = signup_data['email'],
                password = signup_data['password'],
                nickname = signup_data['nickname'],
                phone    = signup_data['phone']
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'message':list(user)}, status=200)


class SignInView(View):
    def post(self, request):
        signin_data = json.loads(request.body)

        try:
            email    = signin_data['email']
            password = signin_data['password']
            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError: 
            return JsonResponse({'message':'KEY ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID USER'}, status=400)