import json

from django.http   import JsonResponse
from django.views  import View
from user.models   import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        email      = data['email']
        phone      = data['phone']
        name       = data['name']
        user_name  = data['user_name']
        password   = data['password']


        try:
            if ('@' not in email or '.' not in email):
                return JsonResponse(
                    {'MESSAGE' : '잘못된 email형식'}, 
                    status = 400
                )
            elif len(password) < 8 :
                return JsonResponse(
                    {'MESSAGE' : 'password는 8자리 이상'}, 
                    status = 400
                )
            elif (User.objects.filter(email = email).exists() 
            or User.objects.filter(user_name = user_name).exists()):
                return JsonResponse(
                    {'MESSAGE' : '이미 사용중'}, status = 400
                )
            else :
                User.objects.create(
                    email      = email,
                    phone      = phone,
                    name       = name,
                    user_name  = user_name,
                    password   = password 
                ).save()
                return JsonResponse(
                    {'MESSAGE' : 'SignUp SUCCESS'}, status = 200
                )
        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KeyERROR'}, status = 400
            )