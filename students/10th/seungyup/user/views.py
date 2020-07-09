import json

from django.views import View
from django.http import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(name=data['name']).exists():
                return JsonResponse({'message': 'EXISTING_ACCOUNT'}, status=401)
            if ('@' in data['email']) and (len(data['password']) >= 5):
                User(
                    name     = data['name'],
                    email    = data['email'],
                    password = data['password']
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            return JsonResponse({'message': "VALIDATION_ERROR"}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    # def get(self, request):
    #     user_data = User.objects.values()
    #     return JsonResponse({'users':list(user_data)}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
            elif User.objects.filter(name = data['name']).exists():
                user = User.objects.get(name=data['name'])

            if user.password == data['password']:
                return JsonResponse({'message': 'SIGN_IN SUCCESS'}, status=200)

            return JsonResponse({'message':'UNAUTHORIZED'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
