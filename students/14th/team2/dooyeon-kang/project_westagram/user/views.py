import json
from django.http import JsonResponse

from django.views import View
from django.db.models import Q
from user.models import User

class UsersView(View):

    def post(self, request):
        data           = json.loads(request.body)
        valid_email    = False
        valid_password = False
        valid_user     = False

        try:
            new_name     = data['name']
            new_email    = data['email']
            new_password = data['password']
            new_phone    = data['phone']
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status = 400)

        #email validation
        if '@' in new_email and '.' in new_email.split('@')[1]:
            valid_email = True
        else:
            return JsonResponse({'message': "Invalid Email"}, status = 400)

        #password validation
        if len(new_password) >= 8:
            valid_password = True
        else:
            return JsonResponse({'message': "Invalid Password"}, status = 400)

        #duplacted value validation
        exist_user = User.objects.filter(Q(name=new_name) | Q(phone=new_phone) | Q(email=new_email))
        if len(exist_user) == 0:
            valid_user = True
        else:
            return JsonResponse({'message': "Name, Phone or Email is already exists"}, status = 400)

        if valid_email and valid_password and valid_user:
            user = User.objects.create(
                name     = new_name,
                email    = new_email,
                phone    = new_phone,
                password = new_password,
            )

            return JsonResponse({'message': "SUCCESS"}, status = 200)
