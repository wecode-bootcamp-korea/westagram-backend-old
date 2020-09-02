import json

from django.views import View
from django.http  import JsonResponse
from .models      import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not '@' in data['email'] or not '.' in data['email']:#이메일 형식이 안 맞을 때
            return JsonResponse({'message':'Email_Form_Error'}, status=400)
        if len(data['pw']) < 8:#비밀번호가 8자리 이하일 때
            return JsonResponse({'message':'Password_Form_Error'}, status=400)
        if (User.objects.filter(email = data['email']) or#이미 있는 이메일, 이름, 폰번호 일 때
            User.objects.filter(name = data['name']) or 
            User.objects.filter(phone_num = data['phone_num'])):
            return JsonResponse({'message':'Already_in_use'}, status=400)
        if not data['email'] or not data['pw']: #이메일, 비밀번호 값이 없을 때
            return JsonResponse({'message':'KEY_ERROR'},status=400)
        else:
            User(
            name      = data['name'],
            email     = data['email'],
            pw        = data['pw'],
            phone_num = data['phone_num']
        ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)#그게 아니면 success 반환

        


    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)

class SignInView(View):   
    def post(self, request):
        data = json.loads(request.body)

        if not data['email'] or not data['pw']: #이메일, 비밀번호 값이 없을 때
            return JsonResponse({'message':'KEY_ERROR'},status=400) #KEY_ERROR 반환
        if User.objects.filter(email=data['email']):#입력한 이메일을 조회 후
            login_user = User.objects.get(email=data['email'])#변수에 저장
            if login_user.pw != data['pw']:#이 변수 사용자의 비밀번호와 입력한 비밀번호가 같지 않을 때
                return JsonResponse({'message':'INVALID_USER'}, status=400)
        else:
            return JsonResponse({'message':'SUCCESSkkk'}, status=200)#아니면 success반환
