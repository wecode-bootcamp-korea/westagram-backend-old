import json

from django.http        import JsonResponse
from django.views       import View

from .models            import Account

MINIMUM_PASSWORD_LENGTH = 8

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try : 
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=400)
        
            else :
                signup = Account.objects.get_or_create(
                    email     = data['email'],
                    name      = data['name'],
                    nickname  = data['nickname'],
                    password  = data['password'],
                    phone     = data['phone']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try :
            email    = data.get('email')
            phone    = data.get('phone')
            nickname = data.get('nickname')
            password = data.get('password')

            if Account.objects.filter(email=email).exists() or\
                Account.objects.filter(phone=phone).exists() or\
                Account.objects.filter(nickname=nickname).exists():
                if Account.objects.filter(password=password):
                    return JsonResponse({'message' : 'SUCCESS'}, status=200)
                else :
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            else :
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError: 
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

