import json, traceback

from django.views import View 
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import User


class Sign_UP_View(View):  #회원가입
    def post(self,request):
        data = json.loads(request.body)
        if not data['email'] or not data['password'] or not data['phone']: # email, password, phone 데이터가 없을 경우
            return JsonResponse({'message' : "KEY ERROR"}, status = 401) # key error, 401로 반환
        try: 
            req_user = User( # 있을 경우
                email    = data['email'],  #각각 데이터를 넣어준다. 
                phone    = data['phone'], 
                password = data['password'], 
            )
            req_user.full_clean()  #각데이터를 넣어준 변수에 유효성 검사를 해준다.
            #form이 모델에서 바로 유효성 검사를 실시하고 싶을 때, 사용하는 메소드이다. 이 메소드를 사용해주어야 실제로 유효성 검사를 실시
        except ValidationError as exceptions:  #유효성검사가 에러났을 경우 처리할 것
            trace_back = traceback.format_exc()
            print(f"{exceptions} : {trace_back}")
            return JsonResponse({'message':trace_back}, status = 200)

        req_user.save()  #유효성 검사가 성공
        return JsonResponse({'message':'SUCCESS'},status = 200)

class Sign_In_View(View) : #로그인
    def post(self, request):  #self는 자기 자신, request는 http요청
        data = json.loads(request.body) #http요청의 body부분을 json형태로 변경

        if not data['email'] or not data['password'] or not data['phone']: #이메일,패스워드,폰의 데이타가 없을 경우
            return JsonResponse({'message' : "KEY ERROR"}, status = 401) # 에러

        if User.objects.filter(email = data['email']).exists(): #필터메소드를 통해 User객체중에 이메일이 존재할 경우
            member = User.objects.get(email = data['email']) #이메일같은 User객체를 member변수에 넣음
            if member.password == data['password'] :  #만약 패스워드 데이터가 같으면
                return JsonResponse({'message':"SUCCESS"}) #로그인
            else:
                return JsonResponse({'message':'INVALID_USER'},status = 401) #패스워드가 맞지 않을 경우
        else : 
            return JsonResponse({'message':'INVALID_USER'},status = 401) #필터메소드를 통해 이메일이 존재하지 않을 경우

        return JsonResponse({'message':'KEY ERROR'},status = 400) #이도저도 아님..












#이메일오류 -> email도 unique라 email로 User객체를 가져온것이다. userid를 가져올 경우 굳이 찾아봐야하고 이메일로 가져오는 게 편해서 바꿔줌