from django.views import View
from django.http  import JsonResponse
import json
import bcrypt
import jwt

from .models      import User

class SignUpView(View):
    def post(self,request):
        signup_data = json.loads(request.body)
        try:
            if User.objects.filter(user_name = signup_data["name"]).exists():
                return JsonResponse({ 'message: ' : 'ID already exists'}, status = 400)
            elif User.objects.filter(user_email = signup_data["email"]).exists():
                return JsonResponse({ 'message: ' : 'Email already exists'}, status = 400)
            elif User.objects.filter(user_phone_number =signup_data["phone_number"]).exists():
                return JsonResponse({ 'message : ' :'phone_number already exists'} , status = 400)
            if  '@' not in signup_data["email"]  or '.' not in signup_data["email"] :
                return JsonResponse({ "message: " : "Invalid email" }, status = 400 )
            elif len(signup_data["password"]) < 8 :
                return JsonResponse({ "message: " : "password validation" } , status = 400 )

            #비밀번호 암호화
            hsshed_password = bcrypt.hashpw(signup_data["password"].encode('utf-8'), bcrypt.gensalt())
            hsshed_password = hsshed_password.decode('utf-8')

            User.objects.create(
                user_name         = signup_data["name"],
                user_email        = signup_data["email"],
                user_phone_number = signup_data["phone_number"],
                user_password     =  hsshed_password
                )
            return JsonResponse ( { 'message: ' : '회원가입 성공!'} , status = 200 )

        except KeyError :
            return JsonResponse( {"message: " : "KEY_ERROR"} , status = 400 )

class LogInView(View):
    def post(self, request):
        try :
            login_data = json.loads(request.body)
            user =  User.objects.get(user_email = login_data["email"])
            password = login_data["password"]
            if User.objects.filter(user_email = login_data["email"]).exists():
                if bcrypt.checkpw(password.encode("utf-8"), user.user_password.encode("utf-8")):
                # ---------------------- 토큰 생성-----------------------
                    SECRET_KEY = 'secret'
                    token= jwt.encode({ 'user_id' : user.id} , SECRET_KEY, algorithm = 'HS256')
                    header = jwt.decode(token , SECRET_KEY , algorithm='HS256')
                    return JsonResponse ({"token" :f"{token}로그인 성공!"} , status = 200)
                else:
                    return JsonResponse ({"message  : ":  "비밀번호가 다릅니다"}, status = 401)
        except  :
            return JsonResponse ({"message : " : "존재하지 않는 아이디입니다."} ,status = 401 )


 #        def get(self, request):
 #            results = []
 #            for users in User.objects.all() :
 #                results.append(User.objects.values())
#            return JsonResponse ({ "data : ":results },status = 200)
#        except  :
#            return JsonResponse({ "message : " : "ERROR"} , status = 200)
