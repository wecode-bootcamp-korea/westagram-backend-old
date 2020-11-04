import json
from django.http  import JsonResponse
from django.views import View
from .models      import User
from .validation   import check_password, check_email

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if check_password(data['password']) or check_email(data['email']):
                return JsonResponse({"message" : 'VALIDATION_ERROR'}, status = 401)
            User(
                name         = data["name"],
                email        = data["email"],
                password     = data["password"],
                phone_number = data["phone_number"],
            ).save()
            return JsonResponse({"message" : "SUCCESS"}, status = 200)    

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(
                name = data["name"],
                email = data["email"],
                password = data["password"],
                phone_number = data["phone_number"]
                ).exists() == True:
                return JsonResponse({"message" : "SUCCESS"}, status = 200)
            else:    
                return JsonResponse({"message" : 'VALIDATION_USER'}, status = 401)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)