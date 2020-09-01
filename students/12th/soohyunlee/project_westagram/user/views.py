import json
import re

from django.views import View
from django.http import JsonResponse
from .models import User

class MainView(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            name      = data['name'],
            email     = data['email'],
            pw        = data['pw'],
            phone_num = data['phone_num']
        ).save()

        if not '@' in data['email'] and not '.' in data['email']:
            return JsonResponse({'message':'Email_Form_Error'}, status=400)
        if len(data['pw']) < 8:
            return JsonResponse({'message':'Password_Form_Error'}, status=400)
        # if User.objects.filter(name = data['name']).exist():
        #     return JsonResponse({'message':'Already_in_use'}, status=400)
        else:
            return JsonResponse({'message':'SUCCESS'}, status=200)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)