import json
from django.views import View
from django.http import JsonResponse, request
from .models import Account

class SignUp(View):

    def post(self, request):
        data = json.loads(request.body) #{name:박승제,number:010-26,email:tmd@djk,password:12345}
        data_key = list(data.keys())

        if 'name' in data_key:
            if Account.objects.all().filter(user_name=data['name']).exists():
                return JsonResponse({"message":"중복된 이름"},status=400)

            if 'number' in data_key:
                if Account.objects.all().filter(user_number=data['number']).exists():
                    return JsonResponse({"message":"중복된 번호"},status=400)

                if 'email' in data_key:
                    if '.' and '@' in data['email']:
                        if Account.objects.all().filter(user_email=data['email']).exists():
                            return JsonResponse({"message":"중복된 email"},status=400)

                        if 'password' in data_key:
                            if Account.objects.all().filter(user_password=data['password']).exists():
                                return JsonResponse({"message":"중복된 password"},status=400)

                            if len(data['password'])>=8:
                                Account.objects.create(user_name      = data['name'],
                                                    user_number   = data['number'],
                                                    user_email    = data['email'],
                                                    user_password = data['password'])
                        
                                return JsonResponse({"massage":"success"}, status= 200)
                            else: 
                                return JsonResponse({"fail":"8자리 이상의 비밀번호를 입력해주세요"},status=400)
                        else:
                            return JsonResponse({'massage':'KEY_ERROR'},status=400)
                    else:
                        return JsonResponse({"fail":"'.'와'@'를 입력하십시오"},status=400)
                else:
                    return JsonResponse({'massage':'KEY_ERROR'},status=400)

            else:
                return JsonResponse({'massage':'KEY_ERROR'},status=400)
        else:
            return JsonResponse({'massage':'KEY_ERROR'},status=400)

class SignUp(View):
    data = json.loads(request.body)

