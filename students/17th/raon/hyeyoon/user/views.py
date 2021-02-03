import json
from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Account

min_length = 8
class UserSignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        name         = data['name']
        password     = data['password']
        email        = data['email']
        phone_number = data['phone_number']
        try:
        #중복ERROR
            if Account.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)

            if Account.objects.filter(name = name).exists():
                return JsonResponse({"MESSAGE":"INVALID_NAME"}, status = 400)

            if Account.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({"MESSAGE":"INVALID_PHONE_NUMBER"}, status = 400)
        
            if len(password) < min_length:
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status = 400)
        
            if '@' not in email or '.' not in email:
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)
        


            Account.objects.create(
                name         = name,
                password     = password,
                email        = email,
                phone_number = phone_number
                )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)
