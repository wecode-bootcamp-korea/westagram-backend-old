import json
import re

from django.db.models     import Q
from django.http          import JsonResponse
from django.views.generic import View

from .models import User

def get_user(name=None, email=None, phone=None):
    if name and email and phone:
        return User.objects.filter(
            Q(name = name) |
            Q(email = email) | 
            Q(phone = phone)
        )
    if name and email:
        return User.objects.filter(Q(name = name) | Q(email = email))
    if name and phone:
        return User.objects.filter(Q(name = name) | Q(phone = phone))
    if email and phone:
        return User.objects.filter(Q(email = email) | Q(phone = phone))
    if name:
        return User.objects.filter(name = name)
    if email:
        return User.objects.filter(email = email)
    if phone:
        return User.objects.filter(phone = phone)
    return None

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = None
            email    = None
            phone    = None
            password = None

            if 'name' in data:
                name = data['name']
            if 'email' in data:
                email = data['email']
            if 'phone' in data:
                phone = data['phone']
            password = data['password']

            if not name and not email and not phone:
                return JsonResponse({
                    'message': 'INVALID_USERNAME'}, 
                    status = 400
                )

            EMAIL_REGEX = "^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$"
            if email and not re.search(EMAIL_REGEX, email):
               return JsonResponse(
                   {'message': 'INVALID_EMAIL'}, 
                   status = 400
                )
            
            if len(password) < 8:
                return JsonResponse(
                    {'message': 'INVALID_PASSWORD'},
                    status = 400
                )

            duplicated_user = get_user(
                name = name, 
                email = email, 
                phone = phone,
            )
            if duplicated_user:
                return JsonResponse(
                    {'message': 'ALREADY_SIGNED_UP_USER'}, 
                    status = 400,
                )
            else:
                User(
                    name     = name,
                    email    = email,
                    phone    = phone,
                    password = password,
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)            

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = None
            email    = None
            phone    = None
            password = None

            if 'name' in data:
                name = data['name']
            if 'email' in data:
                email = data['email']
            if 'phone' in data:
                phone = data['phone']
            password = data['password']

            user = get_user(name=name, email=email, phone=phone)
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status = 401)

            if not password or user.get().password != password:
                return JsonResponse({'message': 'INVALID_USER'}, status = 401)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        return JsonResponse({'message': 'SUCCESS'}, status = 200)