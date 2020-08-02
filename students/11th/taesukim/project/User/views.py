import json
import re

from django.views     import View
from django.http      import JsonResponse

from .models import User

class UserView(View):
    def get(self, request):
        return JsonResponse({'message':'Try Django'}, status = 200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            _email    = data['email']
            _password = data['password']
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        try:
            _phone_number = data['phone_number']
        except KeyError:
            _phone_number = ""
        else:
            if User.objects.filter(phone_number = _phone_number):
                return JsonResponse({'message':'Phone_number is already used'}, status = 400)

        try:
            _name = data['name']
        except KeyError:
            _name = ""
        else:
            if User.objects.filter(name = _name):
                return JsonRespose({'mesaage':'Name is already used'}, status = 400)

        if not re.search('.+[@].+[.].+', _email):
            return JsonResponse({'message':'Email is not correct'}, status = 400)

        if not re.search(".{8,}", _password):
            return JsonResponse({'message':'Password is not correct'}, status = 400)

        if User.objects.filter(email = _email):
            return JsonResponse({'message':'Email is already used'}, status = 400)

        User(
            phone_number = _phone_number,
            name         = _name,
            email        = _email,
            password     = _password
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)
