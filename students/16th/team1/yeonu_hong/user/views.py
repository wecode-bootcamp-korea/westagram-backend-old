import json
from django.http  import JsonResponse
from django.views import View
from .models      import User

# 회원가입
class SignUpView(View):
    def post(self,request): 
        try:
            data      = json.loads(request.body) # JSON으로 들어와서 python dict로 바꿔줌
            name      = data['name']
            phone     = data['phone']
            email     = data['email']
            password  = data['password']
            name_dup  = User.objects.filter(name=data["name"])
            phone_dup = User.objects.filter(phone=data["phone"])
            email_dup = User.objects.filter(email=data["email"])

            if len(password) > 8:
                return JsonResponse({'message': '비밀번호 길이는 8글자 이상'}, status=400)

            if name_dup == name or phone_dup == phone or email_dup == email:
                return JsonResponse({'message': '이미 사용중인 값'}, status=400)

            User(
                name     = name,
                password = password,
                phone    = phone,
                email    = email).save()
    
            return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        # except KeyError as e:
        #     return JsonResponse({'message':e.args[0]}, status=400)

        