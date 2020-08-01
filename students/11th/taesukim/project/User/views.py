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
            if not re.search('.+[@].+[.].+', data['email']):
                return JsonResponse({'message':'Email is not correct'}, status = 400)

            elif not re.search(".{8,}", data['password']):
                return JsonResponse({'message':'Password is not correct'}, status = 400)

            elif User.objects.filter(phone_number = data['phone_number']):
                return JsonRespose({'message':'Phone_number is already used'}, status = 400)

            elif User.objects.filter(name = data['name']):
                return JsonRespose({'mesaage':'Name is already used'}, status = 400)

            elif User.objects.filter(email = data['email']):
                return JsonResponse({'message':'Email is already used'}, status = 400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        User(
            phone_number = data['phone_number'],
            name         = data['name'],
            email        = data['email'],
            password     = data['password']
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)
