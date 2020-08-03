import json

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.db.models import Q

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if '@' and '.' not in data['email']:
                return JsonResponse(
                    {"message":"Email_Not_Verified"},
                    status = 400
                )

            if len(data['password']) < 8:
                return JsonResponse(
                    {"message":"Password_Not_Verified"},
                    status = 400
                )

            User(
                name     = data['name'],
                email    = data['email'],
                phone    = data['phone'],
                password = data['password']
            ).save()
            return HttpResponse(status = 200)
        except IntegrityError:
            return JsonResponse(
                {"message":"Data_Already_Exists"},
                status = 400
            )
        except KeyError:
            return JsonResponse(
                {"message":"KEY_ERROR"},
                status = 400
            )

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(
                Q(name  = data['account']) |
                Q(email = data['account']) |
                Q(phone = data['account'])).exists():
                pass
            else:
                raise User.DoesNotExist

            if User.objects.filter(
                password = data['password']).exists():
                pass
            else:
                raise User.DoesNotExist

            return HttpResponse(status = 200)
        except User.DoesNotExist:
            return JsonResponse(
                {"message":"INVALID_USER"},
                status = 401
            )
        except KeyError:
            return JsonResponse(
                {"message":"KEY_ERROR"},
                status = 400
            )
