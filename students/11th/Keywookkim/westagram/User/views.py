import json, traceback

from django                 import forms
from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import User


class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        signup_db = User.objects.all()
        try:
            user = User(
                account      = data['account'],
                email        = data['email'],
			    password     = data['password'],
                phone_number = data['phone_number']
            )
            user.full_clean()
        # 말미에
            if signup_db.filter(account = data['account']).exists() :
                return JsonResponse({'message':'ID : already exists'}, status=400)
            if signup_db.filter(email = data['email']).exists():
                return JsonResponse({'message':'email : already exists'}, status=400)
            if signup_db.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message':'phone_number : already exists'}, status=400)    
            user.save()
            return JsonResponse({'message':'SUCCESS'}, status=200) 
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValidationError as v :
            trace_back = traceback.format_exc()
            print(f"{v} : {trace_back}")
            return JsonResponse({'message':'Invalid'}, status=400)     

    def get(self, request):
            user_data = User.objects.values()
            return JsonResponse({'This is Newbie\'s data':list(user_data)}, status=200)


# User.objects.filter(name = data['name'], email= data['email'], password = data['password']).exists()


