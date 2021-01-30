import json

from django.http    import JsonResponse
from django.views   import View

from user.models    import User

class SignupView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
        
            if len(data['email']) > 30 or len(data['password']) > 18:
                return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
                
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXIST'}, status=409)

            if len(data['password']) < 8:
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=400)

            email = User.objects.create(
                email    = data['email'],
                password = data['password']
            )

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'REQUEST_WITHOUT_DATA'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            login_user = User.objects.filter(email=data['email'])

            if not login_user.exists() or login_user[0].password != data['password']:
                return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)