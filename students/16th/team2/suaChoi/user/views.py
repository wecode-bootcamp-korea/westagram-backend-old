import json
import re

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignupView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data.get('email')
            phone    = data.get('phone')
            password = data['password']

            email_rule = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            # too short password
            if len(password) <  8:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            # (email & phone) == None
            if email is None and phone is None:
                return JsonResponse({"message": "VALIDATION_ERROR"}, status=400)

            # email != None
            if email is not None:
                # bend email rule
                if not email_rule.match(email):
                    return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
                # exist email
                if User.objects.filter(email=email).exists():
                    return JsonResponse({"message": "EXIST_EMAIL"}, status=400)

            # phone != None
            if phone is not None:
                # exist phone
                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({"message": "EXIST_PHONE_NUMBER"}, status=400)

            User.objects.create(
                 name     = name,
                 email    = email,
                 password = password,
                 phone    = phone
             )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except:
            return JsonResponse({"message":"ERROR"}, status=500)


class LoginView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data.get('email')
            phone    = data.get('phone')
            password = data['password']

            # (email & phone) == None
            if email is None and phone is None:
                return JsonResponse({"message": "VALIDATION_ERROR"}, status=400)

            # email != None
            if email is not None and phone is None:
                # check existed email
                if User.objects.filter(email=email).exists():
                    # check password == password
                    if User.objects.get(email=email).password == password:
                        return JsonResponse({"message": "SUCCESS"}, status=200)
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
                return JsonResponse({"message":"INVALID_EMAIL"}, status=401)

            # phone != None
            elif phone is not None and email is None:
                # check existed phone
                if User.objects.filter(phone=phone).exists():
                    # check password == password
                    if User.objects.get(phone=phone).password == password:
                        return JsonResponse({"message": "SUCCESS"}, status=200)
                    return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
                return JsonResponse({"message":"INVALID_PHONE_NUMBER"}, status=401)

            else:
                return JsonResponse({"message": "DATA_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except:
            return JsonResponse({"message": "ERROR"}, status=500)


