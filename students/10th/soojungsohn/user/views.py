import json
from django.views import View 
from django.http import JsonResponse, HttpResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        if User.objects.filter(name=data['name']).exists():
            return JsonResponse({'message':'EXISTING_ACCOUNT'}, status=401)
        else:
            if ('@' in data['email']) and (len(data['password'])>=5) : 
                User(
                    name    = data['name'],
                    email   = data['email'],
                    password = data['password']
                ).save()
            else:
                return JsonResponse({'message' : 'KEY_ERRORR'}, status=400)
        return JsonResponse({'message':'SUCCESS'}, status=200)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username = data['user']
            password = data['password']
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if User.objects.filter(name=username).exists():
            user = User.objects.get(name=username)
        elif User.objects.filter(email=username).exists():
            user = User.objects.get(email=username)
        
        if user.password == password:
            return HttpResponse(status=200)
        else:
            return JsonResponse({"message":'UNAUTHORIZED'}, status=401)


