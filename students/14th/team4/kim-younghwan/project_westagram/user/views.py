import json
import bcrypt
import jwt 


from django.http                import JsonResponse
from django.views               import View
from django.db.models           import Q

from .models                    import Accounts
from project_westagram.settings import SECRET_KEY, ABC

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'이메일주소 @ 를 넣어주세요 '},status =400)

            if len(data['password']) < 8:
                return JsonResponse({'message':'비밀번호가 너무 짧습니다(최소 8자이상)'},status=400)  
           
            if Accounts.objects.filter(name=data['name'],email=data['email']).exists():
                return JsonResponse({'message' : '이미 존재하는 아이디입니다.'},status=401)  
            else:
                #---비밀번호 암호화---#
                password = data['password'].encode('utf-8')
                password_crypt = bcrypt.hashpw(password,bcrypt.gensalt())
                password_crypt = password_crypt.decode('utf-8')
                Accounts(
                    email       = data['email'],
                    name        = data['name'],
                    password    = password_crypt,
                ).save()

            return JsonResponse({'message': '회원가입완료'},status=201)
        
        except Exception as ex:
            return JsonResponse({'error': f'{ex}'},status=400)
                   
        
class Login(View):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            account = Accounts.objects.get(name = data['name'])
            if bcrypt.checkpw(data['password'].encode('utf-8'),account.password.encode('utf-8')):
                
                #---토큰 발행---#
                token = jwt.encode({'id':account.id},SECRET_KEY,algorithm=ABC)
                token = token.decode('utf-8')
                
                return JsonResponse({'message':f'로그인 성공! token : {token}'},status=201)
            
            else:
                return JsonResponse({'message':'비밀번호가 다릅니다'},status=401)
        
        except Accounts.DoesNotExist:
             return JsonResponse({'message':'아이디가 존재하지 않습니다.'},status=401)

        except Exception as ex:
            return JsonResponse({'Error':f'{ex}'},status=400)
        


