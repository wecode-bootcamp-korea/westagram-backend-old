import json

from django.http            import JsonResponse, request
from django.views           import View
from django                 import forms
from django.core.validators import EmailValidator

from user.models import User

class SignUpView(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            email = data['email']
            phone = data.get(data['phone'], '')
            full_name = data.get(data['full_name'], '')
            user_name = data.get(data['user_name'], '')
            password = data['password']
            date_of_birth = data.get(data['date_of_birth'], '')

            if phone:
                phone = phone.replace('-','')
            
            email_validator(email)
            if len(password) < 8:
                return JsonResponse({'message':'PASSWORD VALIDATION ERROR'}, status=400)
            elif User.objects.filter(email=email).exists() or User.objects.filter(phone=phone).exists() or User.objects.filter(user_name=user_name).exists():
                return JsonResponse({'message':'USER ALREADY EXISTS'}, status=400)

            user = User.objects.create(
                email         = email,
                phone         = phone,
                full_name     = full_name,
                user_name     = user_name,
                password      = password,
                date_of_birth = date_of_birth,
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)            
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except forms.ValidationError:
            return JsonResponse({'message':'EMAIL VALIDATION ERROR'}, status=400)
        except:
            return JsonResponse({"message": "RESPONSE ERROR"}, status=400)

def email_validator(email):
    validator = EmailValidator()
    validator(email)
    return email