import json

from django.views import View
from django.http  import JsonResponse
from .models      import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not '@' in data['email'] or not '.' in data['email']:
            return JsonResponse({'message':'Email_Form_Error'}, status=400)
        if len(data['pw']) < 8:
            return JsonResponse({'message':'Password_Form_Error'}, status=400)
        if (User.objects.filter(email = data['email']) or
            User.objects.filter(name = data['name']) or 
            User.objects.filter(phone_num = data['phone_num'])):
            return JsonResponse({'message':'Already_in_use'}, status=400)
        else:
            User(
            name      = data['name'],
            email     = data['email'],
            pw        = data['pw'],
            phone_num = data['phone_num']
        ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        


    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)

class SignInView(View):   
    def post(self, request):
        data = json.loads(request.body)

        if not data['email'] or not data['pw']: #이메일, 비밀번호 값이 없을 때
            return JsonResponse({'message':'KEY_ERROR'},status=400) #KEY_ERROR 반환
        if User.objects.filter(email=data['email']):
            login_user = User.objects.get(email=data['email'])
            if login_user.pw != data['pw']:
                return JsonResponse({'message':'INVALID_USER'}, status=400)
        else:
            return JsonResponse({'message':'SUCCESSkkk'}, status=200)
