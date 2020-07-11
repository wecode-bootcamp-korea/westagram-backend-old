import json
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        try: 
            if Users.objects.filter(email=data['email']):
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status=401)
            else: 
                Users.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = data['password']
                ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

    def get(self, request):
       user_data = Users.objects.values()
       return JsonResponse({'users':list(user_data)}, status=200)


class SignIn(View): 
    def post(self, request):
        data = json.loads(request.body)
        try:
            input_email=data['email']
            input_password=data['password']
            input_name=data['name']

            if Users.objects.filter(name=input_name).exists():
                user = Users.objects.get(name=data['users'])

            elif Users.objects.filter(email=input_email).exists():
                user = Users.objects.get(email=data['users'])

                if user.password == input_password:
                    return JsonResponse({'message':'Success!'}, status=200)
                
                else:
                    return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)
        
            

##       if Users.objects.filter(email=data['email']):
##            i = Users.objects.get(email=data['email'])
##            if i.password == data['password']:
##                    return JsonResponse({'message':f'{i.email}회원님 로그인 성공'}, status=200)
##            else:
##                    return JsonResponse({'message':'비밀번호 오류'}, status=401)
##
##        return JsonResponse({'message':'INVALID_USER'}, status=400)     

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)


