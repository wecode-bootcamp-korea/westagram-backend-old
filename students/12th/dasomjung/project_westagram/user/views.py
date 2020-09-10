import json
import re
import bcrypt
import jwt
import datetime
from django.views import View
from django.http  import JsonResponse
from .models      import Users



class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        MINIMUM_PASSWORD_LENGTH = 8
        
        try:
            if Users.objects.filter(email=data['email']).exists():   # 아이디(email) 존재할 때
                return JsonResponse({'message': 'Already Exist'}, status = 400)
            
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'WRONG FORM'}, status = 400)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message': 'Too short'}, status=400)   # 에러 반환

            password = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # bytes 데이터 형태로 변환시켜 hash
            decoded_hashed_password = hashed_password.decode('utf-8') # str 데이터 형태로 디코딩해서 db에 저장해야 함
            
            Users.objects.create(
                email    = data['email'],
                password = decoded_hashed_password
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)   # 아이디(eamil)이나 비밀번호 키가 잘못되었을 때
        
  
    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users': list(user_data)}, status=200)


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not Users.objects.filter(email=data['email']).exists():   # 아이디(email) 존재하지 않을때
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            new_password = data['password']   # 새로 입력된 비밀번호
            register_email = Users.objects.get(email = data['email'])  # 이메일 변수에 저장
            password = register_email.password    # 데이터 베이스에 저장된 비밀번호 가져오기

            if not bcrypt.checkpw(new_password.encode('utf-8'), password.encode('utf-8')):
                return JsonResponse({'message':'WRONG_PASSWORD'}, status=401)

            user_id = register_email.id
            SECRET_KEY = ''
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 생성후 만료 시간 30분뒤로 설정
            expire_str = str(expire)   # jwt.encode 할 때는 str 타입으로 바꿔줘야 함
            # 인코딩하여 token 만들기
            encoded_access_token = jwt.encode({'user_id': user_id, 'exp': expire_str}, SECRET_KEY, algorithm = 'HS256')
            # b'토큰' 형태이기 때문에 return 할 때는 str 데이터형으로 변환해야 함
            access_token = encoded_access_token.decode('utf-8')
            
            return JsonResponse({'access_token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)   # 아이디, 비번 계정 전달되지 않았을 때