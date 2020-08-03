import json

from django.views import View
from django.http import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "email already exists"}, status = 400)
            elif not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({"message" : "email form is mismatched"}, status = 400)
            elif len(data['password']) < 8:
                return JsonResponse({"message" : "password form is mismatched"}, status = 400)
            else:
                User(
                    name     = data['name'],
                    email    = data['email'],
                    password = data['password'],
                ).save()
                return JsonResponse({"message" : "SUCCESS"}, status = 200)
        except:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)