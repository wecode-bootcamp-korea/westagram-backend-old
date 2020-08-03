import json, traceback

from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import User


class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            registered_user = User(
            phone_number    = data['phone_number'],
            password        = data['password']
            )
            try:
                registered_user.full_clean()
            except ValidationError as e:
                trace_back = traceback.format_exc()
                print(f'{e} : {trace_back}')
            else:
                registered_user.save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except Exception as e:
            trace_back = traceback.format_exc()
            print(f'{e} : {trace_back}')

        return JsonResponse({'message' : 'try again'}, status = 200)

    def get(self, request):
        return JsonResponse({'get' : 'success'}, status = 200)

