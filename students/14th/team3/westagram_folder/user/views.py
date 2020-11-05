import json
from django.views import View
from django.http import JsonResponse
from .models import Users
# Create your views here.
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            user_name    = data['user_name'],
            phone_number = data['phone_number'],
            email        = data['email'],
            password     = data['password'],
        )
        try:
            if "@" not in data['email'] or "." not in data['email']:
                return JsonResponse({"message" : "email_error"},     status = 400)
            elif len(data['password']) < 8 :
                return JsonResponse({"message" : "short_password"},  status = 400)
            elif Users.objects.filter(email = data['email']).exists() or Users.objects.filter(user_name = data['user_name']).exists() or Users.objects.filter(phone_number = data['phone_number']).exists() :
                return JsonResponse({"message" : "duplicated_information"}, status = 401)
            else:
                Users.objects.create(
                    user_name    = data['user_name'],
                    phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = data['password'],
                    )
                return JsonResponse({"message" : "SUCCESS"},         status = 201)
        except KeyError:
            return  JsonResponse({"message": "KEY_ERROR"}, status = 400)



#            if User.objects.filter(email = data['email']) and User.objects.filter(password = data['password']) != True:
#                #이메일이나 패스워드가 하나라도 전달되지 않았을 시 에러 반환
#                return  JsonResponse({"message": "KEY_ERROR"}, status = 400)
#            elif User.objects.filter(user_name = data['user_name']).exists() or User.objects.filter(phone_number = data['phone_number']).exists() or User.objects.filter(phone_number = data['phone_number']).exists() == True:
#                return JsonResponse({"message" : "중복되는 정보입니다."}, status = 401)
#            elif User.objects.filter(user_name = data['user_name']) and User.objects.filter(email = data['email']) == False:
#                return JsonResponse 에러 처리
#            elif "@" and "." not in User.objects.filter(email = data['email'])
#                return 에러!!!
#            elif User.objects.filter(password = data['password']) <= 8:
#                return 에러 (password validation)
#            else:
#                User.objects.create(user_name = data['user_name'], email = data['email'], password = data['password'])
#                return JsonResponse({"message" : "SUCCESS"}, status = 200)
#            
    