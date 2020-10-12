# autopep8: off
import json
import bcrypt
import re

from django.views import View
from auth.models  import Users
from django.http  import HttpResponse, JsonResponse
from django.db    import IntegrityError


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, data.get('email'))):
            return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
        if len(data.get('password')) < 8:
            return JsonResponse({"message": "WEAK_PASSWORD"}, status=400)

        try:
            if Users.objects.filter(email=data.get('email')).exists():
                return JsonResponse({"message": "EMAIL_TAKEN"}, status=400)
            if Users.objects.filter(name=data.get('name')).exists():
                return JsonResponse({"message": "NAME_TAKEN"}, status=400)
            if Users.objects.filter(phone_number=data.get('phone_number')).exists():
                return JsonResponse({"message": "PHONE_NUMBER_TAKEN"}, status=400)

            password = data.get('password').encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            Users(
                email=data.get('email'),
                password=password_crypt,
                name=data.get('name'),
                phone_number=data.get('phone_number'),
            ).save()

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
