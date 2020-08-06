import json, traceback

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        if not data['email'] or not data['password']:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        try: 
            signup_user = User(
                email    = data['email'],
                password = data['password'],
            )
            signup_user.full_clean()
            signup_user.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except ValidationError as e:
            trace_back = traceback.format_exc()
            print(f"{e} : {trace_back}")
        
        return JsonResponse({'message' : 'Invalid format or Duplicated Email'}, status = 400)

    # 유저 리스트
    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'user' : list(user)}, status = 200)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not data['email'] or not data['password']:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        if User.objects.filter(email = data['email']).exists():
            signin_user = User.objects.get(email = data['email'])
            if signin_user.password == data['password']:
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'user' : list(user)}, status = 200)
