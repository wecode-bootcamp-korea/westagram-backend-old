
import json, re

from django.http        import JsonResponse
from django.views       import View
from django.db import IntegrityError

from user.models        import User



class UserView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            data['name']    = data.get('name')
            data['mobile_number'] = data.get('mobile_number')
            password = data.get('password')
            data['email'] = data.get('email')
            if len(data['password']) < 8:
                return JsonResponse({"message":"password must be at least 8 characters"},status=400)
            email_reg='[a-zA-Z0-9_-]+@[a-z]+.[a-z]'
            email_validation = re.compile(email_reg)

            if re.match(email_validation, str(data.get('email'))):
                return JsonResponse({"message":"it is not a vaild address"},status = 400)

            #중복 검사
            if User.objects.filter(name = data['name']).exists():
                return JsonResponse({'message':'존재하는 이름입니다.'}, status=400)
            if User.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'Number is existed'}, status=400)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'this is not valid address.'}, status=400)

            User.objects.create(
                name         = data['name'] ,
                mobile_number = data['mobile_number'] ,
                email        = data['email'] ,
                password     = data['password'])
            return JsonResponse({'message' : '성공'}, status=200)
        except IntegrityError:
            return JsonResponse(stats=400)

    def get(self,request):
        user_data = list(User.objects.values())
        try:
            return JsonResponse({'data':user_data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'ACCOUNT_DOES_NOT_EXIST'}, status=400)

