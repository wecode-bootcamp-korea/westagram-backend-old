import json

from django.views import View
from django.http  import HttpResponse
from .models      import Account
from django.http  import JsonResponse
import bcrypt     # 암호화에 사용
import jwt        # 토큰 발행에 사용
from westagram.settings import SECRET_KEY

class SignUpView(View) : 
    def post(self,request):
        try: 
            data = json.loads(request.body)
            user_name           =    data['name']
            user_phone_number   =    data['phone_number']
            user_email          =    data['email']
            user_password       =    data['password']

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()) 
            #첫번쨰 파라미터는 암호화할 대상,

            # email validation
            if "@" not in user_email or "." not in user_email: 
                return JsonResponse({"message": "Email_ERRROR"},status = 400)

            # password validation
            if len(user_password) < 8:
                return JsonResponse({"message": "Password_ERRROR"},status = 400)   

            # overlap validation
            if Account.objects.filter(name = user_name).exists():
                return JsonResponse({"message": "Your User Name is overlapped! try again."},status = 400)
            if Account.objects.filter(phone_number = user_phone_number).exists():
                return JsonResponse({"message": "Your Phone Number is overlapped! try again."},status = 400)
            if Account.objects.filter(email = user_email).exists():
                return JsonResponse({"message": "Your Email is overlapped! try again."},status = 400) 
            
            # save to database
            Account(
                name         =    user_name,
                phone_number =    user_phone_number,
                email        =    user_email,
                password     =    hashed_password.decode('utf-8')
            ).save()
            return JsonResponse({"message": "SIGN_UP_SUCCESS"},status = 200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSON_TYPE_Error'}, status = 401)
        except ValueError:
            return JsonResponse({"message": "VALUSE_ERROR"}, status = 400)
    def get(self, request):
      	return JsonResponse({'Hello':'World'}, status = 200)

class SignInView(View):
    def post(self,request):
        try: 
            data = json.loads(request.body)
            input_name           =    data['name']
            input_phone_number   =    data['phone_number']
            input_email          =    data['email']
            input_password       =    data['password']
            
            # print(Account.objects.filter(name = input_name).exists())
            # print(Account.objects.get(name = input_name).password)
            # name validation
        
            if input_name == "" or input_password == "":
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)
            elif Account.objects.filter(name = input_name).exists():
                pwd = Account.objects.get(name = input_name).password.encode('utf-8')
                # if(Account.objects.get(name = input_name).password == input_password):
                if(bcrypt.checkpw(input_password.encode('utf-8'), pwd)):
                    token = jwt.encode({'username' : input_name}, SECRET_KEY, algorithm = "HS256")
                    token = token.decode('utf-8')                          # 유니코드 문자열로 디코딩
                    return JsonResponse({"message" :"LOGIN_SUCESS", "Your_token" : token}, status=200)
                else: 
                    return JsonResponse({'message': "PASSWORD_INCORRECT"}, status = 400)
            else:
                return JsonResponse({"message": "INVALID_USER"}, status = 401) 
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSON_TYPE_Error'}, status = 401)
        except ValueError:
            return JsonResponse({"message": "VALUSE_ERROR"}, status = 400)
    def get(self, request):
        signin_data = Account.objects.values()
        return JsonResponse({'message': list(signin_data)}, status = 200)

    ''' Mission 2
    인스타그램에 회원가입 할 때에는 전화번호, 사용자 이름 또는 이메일이 필수로 필요합니다.
    인스타그램에 회원가입 할 때에는 비밀번호도 필수로 필요합니다.
    이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
    회원가입시 이메일을 사용할 경우, 이메일에는 @와 .이 필수로 포함되어야 합니다. 해당 조건이 만족되지 않을 시 적절한 에러를 반환해주세요. 이 과정을 email validation이라고 합니다.
    회원가입시 비밀번호는 8자리 이상이어야만 합니다. 해당 조건이 만족되지 않을 시, 적절한 에러를 반환해주세요. 이 과정을 password validation이라고 합니다.
    회원가입시 서로 다른 사람이 같은 전화번호나 사용자 이름, 이메일을 사용하지 않으므로 기존에 존재하는 자료와 중복되어서는 안됩니다. 적절한 에러를 반환해주세요.
    회원가입이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
    '''

    ''' Mission 3
    인스타그램에 로그인 할 때에는 전화번호, 사용자 이름 또는 이메일이 필수로 필요합니다.
    인스타그램에 로그인 할 때에는 비밀번호가 필수로 필요합니다.
    계정이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
    계정이 존재하지 않을 때나 비밀번호가 맞지 않을 때, {"message": "INVALID_USER"}, status code 401을 반환합니다.
    로그인이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
    '''