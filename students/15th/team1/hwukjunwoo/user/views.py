import json, re
from django.views     import View
from django.http      import JsonResponse
from user.models import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            data['name'] = data.get('name')
            data['email'] = data.get('email')
            data['phone'] = data.get('phone')
            # if (data['email'] == '') and (data['phone'] == ''):
            #     return JsonResponse({'MESSAGE':'Requred Text(Email or Phone Number)'}, status = 400)
            if data['password'] == '' or data['name'] == '':
                return JsonResponse({'MESSAGE':'Required Text(Name or Password)'}, status = 400)

            r = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if data['email'] != '' and (r.match(str(data['email'])) != None) == False:
                return JsonResponse({'MESSAGE':'EMAIL_VALIDATION'}, status = 400)
            if User.objects.filter(name = data['name']).exists() and (data['name'] != ''):
                return JsonResponse({'MESSAGE':'NAME_DUPLICATED'}, status = 400)
            elif User.objects.filter(email = data['email']).exists() and(data['email'] != ''):
                return JsonResponse({'MESSAGE':'EMAIL_DUPLICATED'}, status = 400)
            elif User.objects.filter(phone = data['phone']).exists() and (data['phone'] != ''):
                return JsonResponse({'MESSAGE':'PHONE_DUPLICATED'}, status = 400)

            if (len(data['password']) < 8):
                return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION'}, status = 400)

            User(
                name = data['name'],
                email = data['email'],
                phone = data['phone'],
                password = data['password'],
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            print(email)
            name = data.get('name')
            print(name)
            phone = data.get('phone')
            print(phone)
            password = data.get('password')
            print(password)

            if name:
                if User.objects.filter(name= name).exists():
                    print('hello')
                    user =User.objects.get(name = data.get('name'))
                    if user.password == data['password']:
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    return JsonResponse({'message': 'INVALID_USER'}, status = 400)
            if email:
                if User.objects.filter(email=email).exists():
                    print('wecode')
                    user = User.objects.get(email=data.get('email'))
                    if user.password == data['password']:
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    return JsonResponse({'message': 'INVALID_USER'}, status = 400)
            if phone:
                if User.objects.filter(phone=phone).exists():
                    print('wework')
                    user= User.objects.get(phone=data.get('phone'))
                    if user.password == data['password']:
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


