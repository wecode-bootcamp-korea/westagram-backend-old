import json, re

from django.http     import JsonResponse
from django.views    import View

from .models         import Account

MINIMUN_PASSWORD_LENGTH = 8

class UserSignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username', None)
            email = data.get('email', None)
            password = data.get('password', None)
            phone_num = data.get('phone_num', None)

            if email and password:
                email_form = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                
                if email_form.match(str(email)):
                    email = email
                else:
                    return JsonResponse({'MESSSAGE': 'INVALID_EMAIL'}, status=400)

                if len(password) < MINIMUN_PASSWORD_LENGTH:
                    return JsonResponse({'MESSSAGE': 'PASSWORD_IS_SHORT'}, status=400)

                if Account.objects.filter(email=data['email']).exists():
                    return JsonResponse({'MESSSAGE': 'ALREADY_USE_EMAIL'}, status=400)

                user_data = Account.objects.create(
                        username = username,
                        email = email,
                        password = password,
                        phone_num = phone_num
                        )

                return JsonResponse({'MESSSAGE': 'SUCCESS'}, status=200)

            return JsonResponse({'MESSSAGE': 'KEY_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'MESSSAGE': 'KEY_ERROR'}, status=400)
