import json
from django.views import View 
from django.http  import JsonResponse 
from .models      import Users

class SignUpView(View):
    
    def post(self , request):
        data =json.loads(request.body)
        try:
                
                name         = data["name"]
                email        = data["email"]
                phone_number = data["phone_number"]
                password     = data["password"]

                a=Users.objects.all()
                for x in a :
                    if name==x.name or email==x.email or phone_number==x.phone_number:
                        return JsonResponse({"Message":"joongbok error"},status=400)
                    
                if len(password)<=8 :
                    return JsonResponse({"Message":"password not invalied"},status=400)
                if email.find('@')==-1 or email.find('.')== -1 :
                    return JsonResponse({"Message":"Email not invalied"},status=400)


                Users.objects.create(name=name, email=email, phone_number=phone_number, password=password)

                return JsonResponse({"Message":"SUCSESS"} , status=200)
            
        except KeyError:
            return  JsonResponse({"Message":"KEY_ERROR"} , status=400)


    
       



# 회원가입시 서로 다른 사람이 같은 전화번호나 사용자 이름, 이메일을 사용하지 않으므로 기존에 존재하는 자료와 중복되어서는 안됩니다. 적절한 에러를 반환해주세요.
# 회원가입이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
# [추가 구현 사항] -> email validation 또는 password validation 과정에서 정규식을 사용해보세요. -ㅅ-?
 
