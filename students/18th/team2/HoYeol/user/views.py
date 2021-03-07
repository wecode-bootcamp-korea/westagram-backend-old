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
        db_name  = User.objects.filter(name=name).exists()

        # 조건들 ()로 묶으면 안되는 이유?
      
        if ('@' or '.') not in list(email):
            return JsonResponse({'ERROR':'email_form'}, status = 401)            

        if len(list(pswd))<8:
            return JsonResponse({'ERROR':'pswd_form'}, status = 401)            

        if db_name is True:
            return JsonResponse({'ERROR':'name_exist'}, status = 401)            
        
        if db_email is True:
            return JsonResponse({'ERROR':'email_exist'}, status = 401)            
        
        if db_phone is True:
            return JsonResponse({'ERROR':'phone_exist'}, status = 401)            
        
        if name or email or phone is None:
            return JsonResponse({'ERROR':'feild_empty'}, status = 401)            

        User.objects.create(name=name, email=email, phone=phone, pswd=pswd)
        return JsonResponse({'SUCCESS':'signup'}, status = 201)
        

class SignInView(View):
    def post(self, request):
   
        data  = json.loads(request.body)
        id    = data['id']
        pswd  = data['pswd']

        db_email = User.objects.filter(email=id).exists()
        db_phone = User.objects.filter(phone=id).exists()
        db_name  = User.objects.filter(name=id).exists()
        db_pswd  = User.objects.filter(pswd=pswd).exists()

        if db_email or db_phone or db_name is False:
            return JsonResponse({'ERROR':'id_not_match'}, status = 401)   

        if id or pswd is None:
            return JsonResponse({'ERROR':'feild_empty'}, status = 401)  

        if db_email or db_phone or db_name is True:
            if db_pswd is False:
                return JsonResponse({'ERROR':'pswd_not_match'}, status = 401) 
            return JsonResponse({'SUCCESS':'signin'}, status = 201)
   


               

