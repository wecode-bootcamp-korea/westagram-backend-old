import json, traceback

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        try: 
            signup_user = User(
                email = data['email'],
                password = data['password'],
            )
            signup_user.full_clean()
        except ValidationError as e:
            trace_back = traceback.format_exc()
            print(f"{e} : {trace_back}")
        else:
            signup_user.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        return JsonResponse({'message' : 'Invalid'}, status=200)

    # 유저 리스트
    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'user' : list(user)}, status = 200)
