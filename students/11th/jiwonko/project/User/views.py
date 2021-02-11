import json, traceback, bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models import User
from .utils import make_token

hashed_password = 0
class Signup(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'Already registered'}, status = 400)
            name = "test_name"
            phone_number = "01012345678"
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User(
                name         = name,
                email        = data['email'],
                password     = hashed_password,
                phone_number = phone_number,
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
                # hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                hashed_password = user
                ps = data['password'].encode('utf-8')
                if bcrypt.checkpw(ps, hashed_password):
                    at = make_token(user.id)
                    return JsonResponse({'access_token' : at}, status = 200)
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
            return JsonResponse({'message' : 'NO_EXISTS_USER'}, status = 404)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
