import json
import re # regular expression

from django.http        import HttpResponse, HttpResponseRedirect, Http404
from django.http        import JsonResponse
from django.shortcuts   import get_object_or_404, render
from django.views       import View

from .models import User

# sign up

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            data_name = data['name']
            data_email = data['email']
            data_password = data['password']
            data_phone = data['phone']        
        except KeyError:
            ## 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        #회원가입시 이메일을 사용할 경우, 이메일에는 @와 .이 필수로 포함. 없으면 적절한 에러를 반환 (email validation)
        email_re = re.compile('.*[@].*[.].*')
        if not email_re.match(data_email):
            return JsonResponse({"message": "EMAIL_VALIDATION_ERROR"}, status=400)

        #회원가입시 비밀번호는 8자리 이상. 해당 조건이 만족되지 않을 시, 적절한 에러를 반환 (password validation)
        if len(data_password) < 8:
            return JsonResponse({"message": "PASSWORD_VALIDATION_ERROR"}, status=400)

        #회원가입시 전화번호, 사용자 이름, 이메일가 기존에 존재하는 자료와 중복되어서는 안됩니다. 
        # 적절한 에러를 반환해주세요.
        name_duplication_chk  = User.objects.filter(name=data_name).values()
        email_duplication_chk = User.objects.filter(email=data_email).values()
        phone_duplication_chk = User.objects.filter(phone=data_phone).values()

        if name_duplication_chk :
            return JsonResponse({"message": "NAME_ALREADY_EXISTS"}, status=400)
        elif email_duplication_chk:
            return JsonResponse({"message": "EMAIL_ALREADY_EXISTS"}, status=400)
        elif phone_duplication_chk:
            return JsonResponse({"message": "PHONE_ALREADY_EXISTS"}, status=400)
        else:
            # 회원가입이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
            User(
                name        = data_name,
                email       = data_email,
                password    = data_password,
                phone       = data_phone
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)



