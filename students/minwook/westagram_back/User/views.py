import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User

class SignUp(View):
    def post(self, request):
        data       = json.loads(request.body)
        current_db = User.objects.all()
        try:
            name     = data['name']
            email    = data['email']
            phone    = data['phone']
            password = data['password']
        except KeyError:
            return JsonResponse({'mwssage':'KEY_ERROR'}, status = 400)

        if name != '' :
            if current_db.filter(name = data['name']):
                return JsonResponse({'message':'DUPLICATE_NAME'}, status = 400)
        elif email != '' :
            if current_db.filter(email = data['email']):
                return JsonResponse({'message':'DUPLICATE_EMAIL'}, status = 400)
        elif phone != '' :
            if current_db.filter(phone = data['phone']):
                return JsonResponse({'message':'DUPLICATE_PHONE'}, status = 400)
        else:
            return JsonResponse({'message':'MINIMUM_CONDITIONS_FAILED'}, status = 400)

        if email != '':
            if ('@' not in email) and ('.' not in email):
                return JsonResponse({'message':'EMAIL_FORMAT_FAILED'}, status = 400)

        if password != '':
            if len(data['password']) < 8:
                return JsonResponse({'message':'SHORT_PASSWORD'}, status = 400)
        User(
            name     = name,
            password = password,
            email    = email,
            phone    = phone
        ).save()
        return JsonResponse({'message':'SUCCESS'}, status = 200)

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status = 200)

class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name     = data['name']
            email    = data['email']
            phone    = data['phone']
            password = data['password']

            if password == '':
                return JsonResponse({'message':'NO_PASSWORD_INPUT'}, status = 400)

            saved_password = ''
            if name != '':
                saved_password = (User.objects.filter(name = name).values().get())['password']
            if email != '':
                saved_password = (User.objects.filter(email = email).values().get())['password']
            if phone != '':
                saved_password = (User.objects.filter(phone = phone).values().get())['password']

            if saved_password != '':
                if password == saved_password:
                    return JsonResponse({'message':'SUCCESS'}, status = 200)
                return JsonResponse({'message':'INVALID_USER'}, status = 401)
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 401)
