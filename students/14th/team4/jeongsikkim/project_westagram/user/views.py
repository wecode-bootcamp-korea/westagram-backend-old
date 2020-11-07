from django.views import View
from django.http import JsonResponse
import json
from django.db.models import Q
from .models import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if "@" not in data['email'] or "." not in data['email']:
                return JsonResponse({"message":"email error!"}, status=400)
            elif len(data['password']) < 8:
                return JsonResponse({"message":"password error!"},status=400)

            elif User.objects.filter(Q(user_id = data['user_id']) |
                                     Q(mobile_number = data['mobile_number']) |
                                     Q(email = data['email'])):
                return JsonResponse({"message":"already in use"}, status=400)

            User.objects.create(
                user_id = data['user_id'],
                mobile_number = data['mobile_number'],
                email = data['email'],
                password = data['password']
            )
            return JsonResponse({"message":"Sign up SUCCESS!"}, status=200)
        except KeyError :
            return JsonResponse({"message":"KeyError!"}, status=400)

class LogInView(View):
    def post(self,request):
        data = json.loads(request.body)
        if 'account' not in data:
            return JsonResponse({"message":"KeyError!"}, status=400)
        if 'password' not in data:
            return JsonResponse({"message":"KeyError!"}, status=400)
        account = User.objects.filter(Q(user_id=data['account']) |
                                       Q(mobile_number=data['account']) |
                                       Q(email=data['account']))
#        print(data)
        if not account:
            return JsonResponse({"message":"invalid Error!"}, status=401)
        if account.values()[0]['password'] != data['password']:
            return JsonResponse({"message":"invalid Error!"}, status=401)

        return JsonResponse({"message":"Log in SUCCESS!"}, status=200)

