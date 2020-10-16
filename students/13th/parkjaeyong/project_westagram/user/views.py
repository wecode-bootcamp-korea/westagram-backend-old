import json
from django.views import View 
from django.http  import JsonResponse 
from .models      import Users
import bcrypt
import jwt
SECRET = 'secret'
db_objects=Users.objects

class SignUpView(View):
    def post(self , request):
        data =json.loads(request.body)
        try: 
                name         = data["name"]
                email        = data["email"]
                phone_number = data["phone_number"]
                password     = data["password"]
                
                get_name  = db_objects.filter(name = name)
                
                hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                hashed_password_d= hashed_password.decode('utf-8')

                if len(get_name) != 0 :
                    return JsonResponse({"Message":"DUPLICATE error"},status=400)

                if len(password)<8 :
                    return JsonResponse({"Message":"password not valid"},status=400)

                if email.find('@')==-1 or email.find('.')== -1 :
                    return JsonResponse({"Message":"Email not valid"},status=400)

                db_objects.create(name=name, email=email, phone_number=phone_number, password=hashed_password_d)

                return JsonResponse({"Message":"SUCCESS"} , status=200)
            
        except KeyError:
            return  JsonResponse({"Message":"KEY_ERROR"} , status=400)

class LoginView(View):
    def post(self , request) :
        try:
            data=json.loads(request.body)
            id       = data["name"]
            password = data["password"]

            get_id_pw        = db_objects.get(name = id)
            password_compare = get_id_pw.password
            hashed_password  = password_compare.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password) :
                access_token = jwt.encode({'id' : 1}, SECRET, algorithm = 'HS256')
                token=access_token.decode('utf-8')
                return JsonResponse({"Message":"SUCCESS", "token":token } , status=200)
                
            else:
                return  JsonResponse({"Message":"INVALID_USER"} , status=401)

        except KeyError:
            return  JsonResponse({"Message":"KEY_ERROR"} , status=400)
    

# 암호화 
# 인스타그램에 로그인 할 때에는 전화번호, 사용자 이름 또는 이메일이 필수로 필요합니다.
# 인스타그램에 로그인 할 때에는 비밀번호가 필수로 필요합니다.
# 계정이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
# 계정이 존재하지 않을 때나 비밀번호가 맞지 않을 때, {"message": "INVALID_USER"}, status code 401을 반환합니다.
# 로그인이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
        


    
       



 
