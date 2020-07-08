import json
from django.http import JsonResponse
from django.views import View
from .models import User

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        if data.get('email',None) == None or data.get('password',None) == None or data.get('name',None) == None:
            return JsonResponse({'message':'email or password or name is vacant'},status=401)
        else:
            User(
                name = data['name'],
                email = data['email'],
                password = data['password']
            ).save()
            return JsonResponse({'message':'Register Success'},status=200)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.get(email=data['email']):
                login_user = User.objects.get(email=data['email'])
                if login_user.password == data['password']:
                    return JsonResponse({'message':'SUCCESS'},status=200)
                else:
                    return JsonResponse({'message':'INVALID_USER'},status=401)
            else:
                return JsonResponse({'message':'INVALID_USER'},status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'},status=400)
