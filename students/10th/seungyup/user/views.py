import json
from django.views import View
from django.http import JsonResponse
from .models import Users

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        Users(
            name = data['name'],
            email = data['email'],
            password = data['password']
        ).save()

        return JsonResponse({'message':'REGISTER_SUCCESS'}, status=200)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)       

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Users.objects.filter(email = data['email']).exists():
            user = Users.objects.get(email = data['email'])
            if user.password == data['password']:
                return JsonResponse({'message': 'SIGN_IN SUCCESS'}, status=200)
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)

        return JsonResponse({'message':'NO_EXISTS_USER'}, status=401)
