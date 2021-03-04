import json

from django.views import View
from django.http  import JsonResponse

from .models import User


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user_name    = data.get('user_name')
            email        = data.get('email')
            password     = data.get('password')
            name         = data.get('name', None)
            phone_number = data.get('phone_number', None)

            if not '@' or not '.' in data['email']:
                return JsonResponse({'message': 'not valid email'}, status=400)

            if len(data['password']) < 8:
                return JsonResponse({'message': 'not valid password'}, status=400)
    
            if User.objects.filter(user_name = user_name).exists():
                return JsonResponse({'message': 'user_name already exists'}, status=400)

            User.objects.create(
                user_name    = user_name,
                email        = email,
                password     = password,
                name         = name,
                phone_number = phone_number,
            )

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        else:
            return JsonResponse({'message': 'SUCCESS'}, status=200)
