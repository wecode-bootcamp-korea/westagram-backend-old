import json
from django.http import JsonResponse
from django.views import View
from .models import Users

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        if data.get('email',None) == None or data.get('password',None) == None:
            return JsonResponse({'message':'email or password is vacant'},status=401)
        else:
            Users(
                    name = data['name'],
                    email = data['email'],
                    password = data['password']
                 ).save()
            return JsonResponse({'message':'Register Success'},status=200)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        if Users.objects.get(email=data['email']):
            login_user = Users.objects.get(email=data['email'])
            if login_user.password == data['password']:
                return JsonResponse({'message':'SUCCESS'},status=200)
            else:
                return JsonResponse({'message':'INVALID_USER'},status=401)
        else:
            return JsonResponse({'message':'INVALID_USER'},status=401)
