import json, traceback, bcrypt, jwt

from datetime               import timedelta
from datetime               import datetime
from django.db              import IntegrityError
from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models import User

SECRET_KEY = 'abc'

class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        if User.objects.filter(phone_number = data['phone_number']).exists():
            return JsonResponse({'message' : 'number already exist'}, status = 400)
        try:
            registered_user = User(
                phone_number    = data['phone_number'],
                password        = data['password']
            )
            registered_user.full_clean()
        except ValidationError:
            trace_back = traceback.format_exc()
            return JsonResponse({'message' : 'validation error'}, status = 400)
        else:
            registered_user.password = bcrypt.hashpw(
                registered_user.password.encode('utf-8'), bcrypt.gensalt())
            registered_user.password =  registered_user.password.decode('utf-8')
            registered_user.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        return JsonResponse({'message' : 'KEY_ERROR'}, status = 406)

class LoginView(View):
    def post(self, request):
        data  = json.loads(request.body)

        if not data['phone_number'] or not data['password']:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        if User.objects.filter(phone_number = data['phone_number']).exists():
            user = User.objects.get(phone_number = data['phone_number'])
            entered_pw = data['password'].encode('utf-8')
            if bcrypt.checkpw(entered_pw, user.password.encode('utf-8')):
                access_token = jwt.encode({'id' : user.id,
                                           'exp' : datetime.now() + timedelta(0,300)},
                                          SECRET_KEY, algorithm='HS256')
                return JsonResponse({'access_token' : access_token.decode()}, status = 200)

        return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

    def get(self, request):
        return JsonResponse({'get' : 'success'}, status = 200)
