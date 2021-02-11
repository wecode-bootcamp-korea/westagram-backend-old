import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import bcrypt
import jwt

from .models import User

class SignUpView(View):
    def post(self, request):
        data       = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password']
        except KeyError:
            return JsonResponse({'mwssage':'KEY_ERROR'}, status = 400)

        if email != '' :
            if User.objects.filter(email = data['email']):
                return JsonResponse({'message':'DUPLICATE_EMAIL'}, status = 400)
        else:
            return JsonResponse({'message':'EMAIL_INFO_EMPTY'}, status = 400)

        if email != '':
            if ('@' not in email) and ('.' not in email):
                return JsonResponse({'message':'EMAIL_FORMAT_FAILED'}, status = 400)

        if password != '':
            if len(data['password']) < 8:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status = 400)
        User(
            email    = email,
            password = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
        ).save()
        return JsonResponse({'message':'SUCCESS'}, status = 200)

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            if password == '':
                return JsonResponse({'message':'NO_PASSWORD_INPUT'}, status = 400)

            saved_password = ''
            if email != '':
                saved_password = User.objects.get(email = email).password

            input_val = password.encode('utf=8')
            if saved_password != '':
                if bcrypt.checkpw(input_val, saved_password.encode('utf-8')):
                    login_token = jwt.encode({'user_id' : User.objects.get(password = saved_password).id}, 'Salt', algorithm = 'HS256')
                    return JsonResponse({'message':login_token.decode('utf-8')}, status = 200)
                return JsonResponse({'message':'INVALID_PW'}, status = 401)
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_EMAIL'}, status = 401)
