import json
from django.http  import JsonResponse
from django.views import View
from .models      import User

# 회원가입
class SignUpView(View):
    def post(self,request): 
        data     = json.loads(request.body)
        print(data['name'])
        print(User.objects.filter(name=data["name"])) #  쿼리셋[] 비어있음

        name     = User.objects.filter(name=data['name'])
        phone    = User.objects.filter(phone=data['phone'])
        email    = User.objects.filter(email=data['email'])
        password = User.objects.filter(password=data['password'])
        print(name, phone, email, password)

        if password.exists():
            if len(password) >= 8:
                if name.exists() or phone.exists() or email.exists():
                    if name.count() and phone.count() and email.count() < 2:
                        User(
                            name     = data['name'],
                            password = data['password'],
                            phone    = data['phone'],
                            email    = data['email']).save()
                
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'message': '이미 사용중인 값'}, status=400)
                else:
                    return JsonResponse({'message': '누란된 값이 있음'}, status=400)
            else:
                return JsonResponse({'message': '비밀번호 길이는 8글자 이상'}, status=400)
        else:
            return JsonResponse({'message': '비밀번호 없음'}, status=400)