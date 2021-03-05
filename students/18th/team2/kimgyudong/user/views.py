import json

from django.views import View
from django.http  import JsonResponse

from .models import User

class UserSignUp(View):
    def post(self,request):
        data = json.loads(request.body)
        
        if "email" not in data or "password" not in data:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

        email    = data["email"]
        password = data["password"]

        
        
        if len(password) < 8:
            pass



