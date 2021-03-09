import json
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q



from .models     import User
from my_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):

        try:
            data         = json.loads(request.body)
            username     = data['username']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            if email == '' or password == '' :
                return JsonResponse({'message':'이메일과 패스워드를 채워주세요' }, status=400)

            if '@' not in email or '.' not in email :
                return JsonResponse({'message':'잘못된 형식입니다. 이메일을 다시한번 확인해 주세요'}, status=400)
            
            if User.objects.filter(Q(email=email) | Q(username=username) | Q(phone_number=phone_number)):
                return JsonResponse({'message':'이미 가입되어 있습니다.'}, status=400)

            if len(password) < 8:
                return JsonResponse({'message':'비밀번호 8자리 이상 입력해 주세요.'}, status=400)

            password = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            User.objects.create(username=username, email=email, password=password_crypt.decode('utf-8'), phone_number=phone_number)
            return JsonResponse({'message':'회원가입 되었습니다.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDECODE_ERROR"}, status = 400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):

        try:
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']
            user_name     = data['username']
            user_phone    = data['phone_number']

            if user_email == '':
                return JsonResponse({'message':'이메일을 입력해주세요.'}, status=400)
            
            if user_password == '':
                return JsonResponse({'message':'비밀번호를 채워주세요.'}, status=400)

            user_account = User.objects.get(email=user_email)
            if bcrypt.checkpw(user_password.encode('utf-8'), user_account.password.encode('utf-8')):
                access_token = jwt.encode({'user_id':'user_acount.id'}, 'SECRET', algorithm='HS256')
                return JsonResponse({'token': access_token, 'message':'SUCCESS'}, status=200)
            return JsonResponse({'message':'INVALID_USER'}, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({"message": "JSONDECODE_ERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
