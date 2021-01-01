import json
import re

from django.http  import JsonResponse
from django.views import View

from .models import User

class UserView(View):

    def post(self, request):
         data = json.loads(request.body)
         name = data['name']
         email = data['email']
         password = data['password']

         email_rule = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

         try:
             # KEY ERROR
             if not email and password:
                 return JsonResponse({"message": "KEY_ERROR"}, status=400)

             # too short password
             if len(password) <  8:
                 return JsonResponse({"message":"NOT_VALID_PASSWORD"}, status=400)

             # bend email rule
             if not email_rule.match(email):
                 return JsonResponse({"message": "NOT_VALID_EMAIL"}, status=400)

             # exist email
             if User.objects.filter(email=email).exists():
                 return JsonResponse({"message": "EXIST_EMAIL"}, status=400)

             if not User.objects.filter(email=email).exists():
                 User.objects.create(
                     name = name,
                     email = email,
                     password = password
                 )
                 return JsonResponse({"message": "SUCCESS"}, status=200)

         except:
             return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({"user": list(user)}, status=200)

