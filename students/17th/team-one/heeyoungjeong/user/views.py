import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from json.decoder import  JSONDecodeError
from user.models import User

class SignUp(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            check_lst = ['name', 'user_name', 'email', 'password']
            for key in check_lst:
                if key not in data.keys():
                    return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({'message':'The email is not valid'}, status=400)

            if not 8 <= len(data['password']):
                return JsonResponse({'message': 'The password is not valid'}, status=400)

            user = User.objects.filter(email=data['email'])

            if not user:
                User.objects.create(
                    name      = data['name'],
                    user_name = data['user_name'],
                    email     = data['email'],
                    password  = data['password'],
                )
                return JsonResponse({'message':'SUCCESS'}, status=200)

            else:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

