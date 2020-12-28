import json, re, bcrypt, jwt #파이썬 내장 모듈
from django.views     import View #장고 제공 모듈
from django.http      import JsonResponse 
from user.models import User #직접 구현한 app 관련 파일들


class SignUpView(View):
    def post(self, request):
        r = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        try:
            data     = json.loads(request.body)
            name     = data.get('name')
            email    = data.get('email')
            phone    = data.get('phone')
            password = data.get('password')
            
            if data['email'] == '' and data['phone'] == '' and  data['name'] == '':
                return JsonResponse({'MESSAGE':'Requred Text(Email or Phone Number or name)'}, status = 400)
            if data['password'] == '':
                return JsonResponse({'MESSAGE':'Required Text(Password)'}, status = 400)

            if data.get('email'):
                if data['email'] != '' and (r.match(str(data['email'])) != None) == False:
                    return JsonResponse({'MESSAGE':'EMAIL_VALIDATION'}, status = 400)
                    if User.objects.filter(email = data['email']).exists() and(data['email'] != ''):
                        return JsonResponse({'MESSAGE':'EMAIL_DUPLICATED'}, status = 400)
            if data.get('name'):
                if User.objects.filter(name = data['name']).exists() and (data['name'] != ''):
                    return JsonResponse({'MESSAGE':'NAME_DUPLICATED'}, status = 400)
            if data.get('phone'):
                if User.objects.filter(phone = data['phone']).exists() and (data['phone'] != ''):
                    return JsonResponse({'MESSAGE':'PHONE_DUPLICATED'}, status = 400)        
            if len(data['password']) < 8:
                return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                name = data.get('name'),
                email = data.get('email'),
                phone = data.get('phone'),
                password = data.get('password'),
                hashed_password = hashed_password,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class LoginView(View):
    def post(self, request):

        data            = json.loads(request.body)
        email           = data.get('email')
        name            = data.get('name')
        phone           = data.get('phone')
        password        = data['password']
        hashed_password = data.get('hashed_password')     
        try: 
            if name:
                if User.objects.filter(name= data.get('name')).exists():
                    user =User.objects.get(name = name)
                    if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                        token = jwt.encode({'name': user.name}, 'SECRET_KEY', algorithm = 'HS256') 
                        return JsonResponse({'MESSAGE':'SUCCESS','TOKEN': token.decode('UTF-8')}, status =200) 
                return JsonResponse({'message': 'INVALID_USER'}, status = 400)
            
            if email:
                if User.objects.filter(email=data.get('email')).exists():
                    user = User.objects.get(email=email)
                    if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                        token = jwt.encode({'email': user.email}, 'SECRET_KEY', algorithm = 'HS256') 
                        return JsonResponse({'MESSAGE':'SUCCESS','TOKEN': token.decode('UTF-8')}, status =200) 
                return JsonResponse({'message': 'INVALID_USER'}, status = 400)
            
            if phone:
                if User.objects.filter(phone=data.get('phone')).exists():
                    user= User.objects.get(phone=phone)
                    if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                        token = jwt.encode({'phone': user.phone}, 'SECRET_KEY', algorithm = 'HS256') 
                        return JsonResponse({'MESSAGE':'SUCCESS','TOKEN': token.decode('UTF-8')}, status =200) 
                return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
