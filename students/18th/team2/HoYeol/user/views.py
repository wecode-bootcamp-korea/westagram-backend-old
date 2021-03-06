# from westagram.settings import AUTH_PASSWORD_VALIDATORS
# from django.core.exceptions import ViewDoesNotExist
import json
from django.db.models.expressions import Exists
from django.views    import View
from django.http     import JsonResponse
from .models         import User

class SignUpView(View):
    def post(self, request):
        
        data  = json.loads(request.body)
        name  = data['name']
        email = data['email']
        phone = data['phone']
        pswd  = data['pswd']

        db_email = User.objects.filter(email=email).exists()
        db_phone = User.objects.filter(phone=phone).exists()

        if ('@' or '.') not in list(email):
            return JsonResponse({'result':'email_form_error.'}, status = 401)            

        if len(list(pswd))<8:
            return JsonResponse({'result':'pswd_form_error.'}, status = 401)            

        if db_email is True:
            return JsonResponse({'result':'email_exist_error.'}, status = 401)            
        
        if db_phone is True:
            return JsonResponse({'result':'phone_exist_error.'}, status = 401)            

        else:
            User.objects.create(name=name, email=email, phone=phone, pswd=pswd)
            return JsonResponse({'result':'signup_done'}, status = 201)
        

        

