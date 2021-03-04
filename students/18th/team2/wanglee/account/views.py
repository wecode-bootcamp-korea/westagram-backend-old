import json
from django.views import View
from django.http  import JsonResponse
from .models      import User

class UserSignup(View):
    def post(self, request):
        users    = User.objects.all()
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        username = data['username']
        phone    = data['phone']

        if email == '' or password == '':
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        elif '@' not in email or '.' not in email:
            return JsonResponse({"message":"email must contain the '@' symbol and the period'.'"}, status=400)
        
        elif len(password) < 8:
            return JsonResponse({"message":"password must be at least 8 characters"}, status=400)
        else:
            for user in users:
                if username == user.username:
                    return JsonResponse({"message":"That username is taken. Try another"}, status=400)
                elif email  == user.email:
                    return JsonResponse({"message":"That email is taken. Try another"}, status=400)
                elif phone  == user.phone:
                    return JsonResponse({"message":"That phone number is taken. Try another"}, status=400)

            User.objects.create(username=username, email=email, password=password, phone=phone)
            return JsonResponse({'result': 'SUCCESS'}, status=200)
        