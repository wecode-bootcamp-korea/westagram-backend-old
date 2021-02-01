import json

from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models      import Userinfo

# 회원가입
class UserSignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        password_validity = data['password']
        try:
            if Userinfo.objects.filter(name = data['name']).exists():
                return JsonResponse({"MESSAGE" : "Invailed_Name_Syntax"}, status = 403)
        
            if Userinfo.objects.filter(Phone_number = data['phone_number']).exists():
                return JsonResponse({"MESSAGE": "Inavailed_Number_Syntax"}, status= 403)
        
            if Userinfo.objects.filter(email = data['email']).exists():
                return JsonResponse({"MESSAGE":"Inavailed_Email_Syntax"}, status = 403)
        
            if '@' and '.' not in data['email']:
                return JsonResponse({"MESSAGE" : "Inavailed_KeyError"}, status= 403)
        
            if len(password_validity) < 8:
                return JsonResponse({"MESSAGE" : "Sure?"}, status= 403)

            Userinfo.objects.create(
                    name         = data['name'],
                    Phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = data['password']
                    )
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)

# 로그인
class UserLoginView(View):
    def POST(self, request):
        data = json.loads(request.body)

        if Userinfo.objects.filter(name = data['name']) or Userinfo.objects.filter(Phone_number = data['phone_number']) or Userinfo.objects.filter(email = data['email']) or Userinfo.objects.filter(  )



