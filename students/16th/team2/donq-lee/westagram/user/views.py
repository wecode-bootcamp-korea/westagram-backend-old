import json
from django.views import View
from django.http  import JsonResponse
from user.models  import User

class UserSignUpView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        phone    = data['phone']
        name     = data['name']
        nickname = data['nickname']
        password = data['password']
        
        if not (email or phone) and name and nickname and password:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        if email == '':
            if User.objects.filter(phone = phone).exists():
                return JsonResponse({'message':'EXIST_NUMBER'}, status = 400)
            if User.objects.filter(nickname = nickname).exists():
                return JsonResponse({'message':'EXIST_NICKNAME'}, status = 400)
        if phone == '':
             if User.objects.filter(email = email).exists():
                return JsonResponse({'message':'EXIST_EMAIL'}, status = 400)
             if User.objects.filter(nickname = nickname).exists():
                return JsonResponse({'message':'EXIST_NICKNAME'}, status = 400)
        if len(password) < 8:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
        if email !='':
            if '@' not in email or '.' not in email:
                return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        User.objects.create(
            email    = email,
            phone    = phone, 
            name     = name, 
            nickname = nickname, 
            password = password
            )
        return JsonResponse({'message':'SUCCESS'}, status = 200)

class UserSignInView(View):
    def post(self, request):
        data      = json.loads(request.body)
        email     = data.get('email')
        phone     = data.get('phone')
        nickname  = data.get('nickname')
        password  = data.get('password')

        if email is not None:
            if User.objects.filter(email = email).exists():
                if User.objects.get(email = email).password == password:
                    return JsonResponse({'message': 'SIGN_IN_SUCCESS'}, status = 200)
                else:
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)
            else:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)
        if phone is not None:
            if User.objects.filter(phone = phone).exists():
                if User.objects.get(phone = phone).password == password:
                    return JsonResponse({'message': 'SIGN_IN_SUCCESS'}, status = 200)
                else:
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)
            else:
                return JsonResponse({'message': 'INVALID_PHONE'}, status =400)
        if nickname is not None:
            if User.objects.filter(nickname = nickname).exists():
                if User.objects.get(nickname = nickname).password == password:
                    return JsonResponse({'message': 'SIGN_IN_SUCCESS'}, status = 400)
                else:
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)
            else:
                return JsonResponse({'message': 'INVALID_NICKNAME'}, status =400)


    



