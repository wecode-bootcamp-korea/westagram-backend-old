import json,re

from django.http     import JsonResponse
from django.views    import View

from user.models     import User

'''
localhost:8000/signup post요청으로 회원가입 요청시, 
1. 이메일 유효성 검사(정규표현식 이용)
http -v POST localhost:8000/signup email="milesmin23gmail.com" phone_number="010-5717-6080" password="123456789"
2. 비밀번호 8자이상일때만 회원가입 가능 로직
http -v POST localhost:8000/signup email="milesmin23@gmail.com" phone_number="010-5717-6080" password="1234"
3. 핸드폰번호 유효성검사(정규표현식 이용)
http -v POST localhost:8000/signup email="milesmin23@gmail.com" phone_number="01057176080" password="123456789"
4. 입력값이 부족할경우, 예외처리를 통해서 서버다운현상 방지
'''
class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if bool(re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data["email"])):
                if bool(re.match('(\d{3}).*(\d{3}).*(\d{4})', data["phone_number"])):
                    if len(data["password"]) >= 8:
                        User.objects.create(email=data["email"], phone_number=data["phone_number"], password=data["password"])
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
                    else:
                        return JsonResponse({'MESSAGE':'Password is short'}, status=400)
                else:
                    return JsonResponse({'MESSAGE':'INVALIDE_PHONE_NUMBER'}, status=400)
            else:
                return JsonResponse({'MESSAGE':'INVALIDE_EMAIL'}, status=400)
                
        except KeyError:

            return JsonResponse({'MESSAGE':'INVALIDE_KEY'}, status=400)

'''
localhost:8000/signin post요청으로 로그인 요청시, 
1. 입력받은 이메일과 패스워드가 db의 것과 일치하는지 여부 체크
http -v POST localhost:8000/signin email="milesmin23@naver.com" password="123456789"
http -v POST localhost:8000/signin email="milesmin23@gmail.com" password="123456789"
2. 입력값이 부족할경우, 예외처리를 통해서 서버다운현상 방지

'''
class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_email = data['email']
            user_password = data['password']
            
            if User.objects.filter(email=user_email):
                user = User.objects.filter(email=user_email).first()
                if user.password == user_password:
                    return JsonResponse({'message':'login success'}, status=400)
                    #return HttpResponse(status=200)
                else:
                    return JsonResponse({'message':'INVALIDE_PASSWORD'}, status=400)
            else:
                return JsonResponse({'message':'EMAIL_NOT_FOUND'}, status=400)
        except KeyError:
            return JsonResponse({'message':'INVALIDE_KEY'}, status=400)
