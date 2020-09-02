import json

from django.views import View
from django.http import JsonResponse
from .models import User

class MainView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not '@' in data['email'] or not '.' in data['email']:
            return JsonResponse({'message':'Email_Form_Error'}, status=400)
        if len(data['pw']) < 8:
            return JsonResponse({'message':'Password_Form_Error'}, status=400)
        if (User.objects.filter(email = data['email']) or
            User.objects.filter(name = data['name']) or 
            User.objects.filter(phone_num = data['phone_num'])):
            return JsonResponse({'message':'Already_in_use'}, status=400)
        else:
            return JsonResponse({'message':'SUCCESS'}, status=200)

        User(
            name      = data['name'],
            email     = data['email'],
            pw        = data['pw'],
            phone_num = data['phone_num']
        ).save()


    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)