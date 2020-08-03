import json, traceback

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import User

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            registered_user = User(
            phone_number    = data['phone_number'],
            password        = data['password']
            )
            registered_user.full_clean()
        except ValidationError as e:
            trace_back = traceback.format_exc()
            print(f'{e} : {trace_back}')
        else:
            registered_user.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        return JsonResponse({'message' : 'try again'}, status = 406)

    def get(self, request):
        return JsonResponse({'get' : 'success'}, status = 200)

class LoginView(View):
    def post(self, request):
        data  = json.loads(request.body)
        users = User.objects.all()

        if not data['phone_number'] or not data['password']:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        if users.filter(phone_number = data['phone_number']):
            user = users.get(phone_number=data['phone_number'])
            if user.password == data['password']:
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

    def get(self, request):
        return JsonResponse({'get' : 'success'}, status = 200)
