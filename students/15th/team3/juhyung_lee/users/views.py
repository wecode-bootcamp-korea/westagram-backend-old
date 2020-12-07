import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import User


class SignUpView(View):
    def post(self, request):
        try:
            data                 = json.loads(request.body)
            data['username']     = data.get('username')
            data['email']        = data.get('email')
            data['phone_number'] = data.get('phone_number')

            if User.objects.filter(Q(username=data['username']) & Q(email=data['email']) & Q(phone_number=data['phone_number'])).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status = 400)

            if data['email'] is not None and ('@' not in data['email'] or '.' not in data['email']):
                return JsonResponse({'message': 'WRONG_FORM'}, status = 400)

            if len(data['password']) < 8:
                return JsonResponse({'message': 'TOO_SHORT_PASSWORD'}, status = 400)

            User(
                username        = data['username'],
                email           = data['email'],
                phone_number    = data['phone_number'],
                password        = data['password'],
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        data         = json.loads(request.body)
     #   username     = data['username']
     #   email        = data['email']
     #   phone_number = data['phone_number']
     #   password     = data['password']

        if User.objects.filter(Q(username=data['username']) | Q(email=data['email']) | Q(phone_number=data['phone_number'])).exists():
            if User.objects.filter(Q(password=data['password']).exists():
                return JsonResponse({'message': 'SUCCESS'}, status = 200)




      #  if User.objects.filter(Q(username=data['username']) | Q(email=data['email']) | Q(phone_number=data['phone_number'])) is not None:
      #      user = User.objects.get(Q(username=data['username']) & Q(email=data['email']) & Q(phone_number=data['phone_number']))
       #     if user.password == data['password']:
        #        return JsonResponse({'message': 'SUCCESS'}, status = 200)
#            elif user.pssword == data['password']:
 #               return JsonResponse({'message': 'INVALID_USER'}, status = 401)

     #   except KeyError:
            #return JsonResponse({'message': 'KEY_ERROR'}, status = 400)




    # *** 지켜야 할 점들 ***
    # - 에러코드도 일정하게 (대문자로 만들었다면 전체 스타일 통일)
    # - 불 필요한 else나 조건 쓰지 않기 (이미 값이 True나 False라면 '== 0' 같은 조건은 불필요)
    # - 코드 컨벤션 (import 코드 정렬 / = 코드 정렬)



    # 안 쓰는 코드들
    # if request.method == "POST":
    # if User.objects.filter(email=data['email']).exists():
    # User.objects.create(username=request.Post['username'], password[request.use]
