import json, re
from django.views     import View
from django.http      import JsonResponse
from user.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if (data['email'] == '') and (data['phone'] == ''):
                return JsonResponse({'MESSAGE':'Requred Text(Email or Phone Number)'}, status = 400)
            if data['password'] == '' or data['name'] == '':
                return JsonResponse({'MESSAGE':'Required Text(Name or Password)'}, status = 400)

            r = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if (data['email'] != '') and (r.match(str(data['email'])) != None) == False:
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

# class SignUpView(View):
#     def post(self, request):
#         data = json.loads(request.body)
