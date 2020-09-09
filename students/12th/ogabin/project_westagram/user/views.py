import json
from django.http  import JsonResponse
from django.views import View
from .models      import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            name         = data["name"],
            email        = data["email"],
            password     = data["password"],
            phone        = data["phone"],
        ).save()
        return JsonResponse({"message":"SUCCESS"}, status = 200)    

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'User':list(user_data)}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            User(
                name         = data["name"],
                email        = data["email"],
                password     = data["password"],
                phone        = data["phone"],
            )

            if User.objects.filter(name = data["name"], password = data["password"], email = data["email"]).exists() == True:
                return JsonResponse({"message": "SUCCESS"}, status = 200)
            else:
                return JsonResponse({"message": "INVALID_USER"}, status = 401)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400) 

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"list" : list(user)}, status = 200)
    
