import json

from django.views import View
from django.http  import JsonResponse

from .models      import User

class SignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': "EXIST_EMAIL"}, status=400)
            if ('@' in data['email']) and (len(data['password']) >= 5):
                User(
                    name = data['name'],
                    email = data['email'],
                    password = data['password']
                ).save()
                return JsonResponse({'message': 'PERMISSION_MEMBERS'}, status=200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    def get(self, request):
        user_data = user.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)

class SignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(name=data['name']).exists and User.objects.filter(password=data['password']).exists:
                return JsonResponse({'message':'LOG_IN_SUCCESS'}, status=200)
        except:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
