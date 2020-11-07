import json
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import User

class UserView(View):
    def post(self, request):
        email_check          = re.compile('^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
        password_check       = re.compile(r'^.*(?=.{8,18})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@#£$%^&*()_+={}\-?:~\[\]]+$')
        phone_check          = re.compile('(\d{3})(\d{3,4}\d{4})')
        name_check           = re.compile('^[a-zA-Z0-9]+(([^,. !@#$%^&*()\'\";:<>?\/ = +|`~][a-zA-Z])?[a-zA-Z]*)*$')
        data                 = json.loads(request.body)

        if not 'email' in data or not 'password' in data or not 'name' in data or not 'phone' in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        if not re.match(name_check, data['name']) or len(data['name']) > 15 or len(data['name']) < 3:
            return JsonResponse({'message':'BAD_NAME_REQUEST'}, status=400)
        if not re.match(email_check,data['email']):
            return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)
        if not re.match(password_check,data['password']) or len(data['password']) < 8: 
            return JsonResponse({'message':'BAD_PASSWORD_REQUEST'},status=400)
        if not re.match(phone_check, data['phone']) or len(data['phone']) > 11 or len(data['phone']) < 10:
            return JsonResponse({'message':'BAD_PHONE_NUMBER_REQUEST'}, status=400)
        if User.objects.filter(Q(name=data['name']) | Q(email=data['email']) | Q(phone=data['phone'])):    
            return JsonResponse({'message':'USER_EXISTS'}, status=400)

        User.objects.create(
            name     = data['name'],
            email    = data['email'],
            phone    = data['phone'],
            password = data['password'],
        )

        return JsonResponse({'message':'SUCCESS'},status=200)
    
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if ('name' not in data and 'phone' not in data and 'email' not in data) or ('password' not in data) or len(data) != 2:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        user_info = [value for key, value in data.items() if key != 'password']

        try:
            user = User.objects.filter(Q(name=user_info[0]) | Q(email=user_info[0]) | Q(phone=user_info[0]))
            if not user:
                raise User.DoesNotExist
            if user[0].password != data['password']:
                raise User.DoesNotExist
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

