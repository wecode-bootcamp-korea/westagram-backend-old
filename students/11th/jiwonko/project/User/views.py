import json, traceback

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models import User

class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        if User.objects.filter(email = data['email']).exists():
            return JsonResponse({'message' : 'Already registered'}, status = 400)
        try:
            user = User(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number']
            )
            user.full_clean()
        except ValidationError as e:
            trace_back = traceback.format_exc()
            print(f"{e} : {trace_back}")
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        else:
            user.save()
            return JsonResponse({'message' : 'Register_Success'}, status = 200)
        return JsonResponse({'message' : 'INVALID_FORMAT'}, status = 400)

class Signin(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if user.password == data['password']:
                    return JsonResponse({'message' : f'{user.email} Success'}, status = 200)
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            return JsonResponse({'message' : 'NO_EXISTS_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
