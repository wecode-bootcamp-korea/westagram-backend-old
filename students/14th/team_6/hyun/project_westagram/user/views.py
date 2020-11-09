from django.views import View
from .models import User
from django.http import JsonResponse
import json

class SignUpView(View):
    def post(self,request):
        signup_data = json.loads(request.body)
        try:

            if User.objects.all().filter(
                user_name = signup_data["name"]).exists():
                return JsonResponse(
                { 'message: ' : 'ID already exists'}, status = 400)
            elif User.objects.all().filter(
                user_email = signup_data["email"]).exists():
                return JsonResponse(
                { 'message: ' : 'Email already exists'}, status = 400)
            elif User.objects.all().filter(user_phone_number =
                    signup_data["phone_number"]).exists():
                return JsonResponse(
                { 'message : ' :'phone_number already exists'} , status = 400)

            if User.objects.all().filter(
                user_email    = signup_data["email"],
                user_password = signup_data["password"]
                ).exists():
                return JsonResponse ( {"message: " : "KEY_ERROR"}, status = 400)
            elif  '@' not in signup_data["email"]  or '.' not in signup_data["email"] :
                return JsonResponse(
                    { "message: " : "Invalid email" }, status = 400 )
            elif len(signup_data["password"]) < 8 :
                return JsonResponse(
                    { "message: " : "password validation" } , status = 400 )

            User.objects.create(
                user_name         = signup_data["name"],
                user_email        = signup_data["email"],
                user_phone_number = signup_data["phone_number"],
                user_password     = signup_data["password"]
            )

            return JsonResponse ( { 'message: ' : '회원가입 성공!'} , status = 200 )

        except KeyError :
            return JsonResponse( {"message: " : "ERROR"} , status = 400 )

class LogInView(View):
    def post(self, request):
        login_data = json.loads(request.body)
#        try :
        User (
            user_name     = login_data["name"],
            user_password = login_data["password"],
#                user_email    = login_data["email"] ,
#                user_phone_number = login_data["phone_number"] ,
        )
        if User.objects.filter(
            user_name = login_data["name"],
            user_password =login_data["password"]).exists():
            return JsonResponse ({"message : " : " 로그인 성공"} , status = 200)
        elif User.objects.filter(user_name = login_data["name"]).exist == False:
            return JsonResponse (
                {"message : " : "존재하지 않는 아이디입니다"} ,
                status = 401 )
        elif User.objects.filter(
            user_password = login_data["password"]).exist==False :
            return JsonResponse (
                {"message  : ":  "비밀번호가 다릅니다"}, status = 401)
    def get(self, request):
        results = []
        for users in User.objects.all() :
            results.append(User.objects.values())
        return JsonResponse ({ "data : ":results },status = 200)
#        except  :
#            return JsonResponse({ "message : " : "ERROR"} , status = 200)
