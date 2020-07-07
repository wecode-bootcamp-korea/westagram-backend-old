from django.shortcuts import render
import json
from django.views import View 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Users, Comment
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        if Users.objects.filter(name=data['name']).exists():
            return JsonResponse({'message':'EXISTING_ACCOUNT'}, status=401)
        else:
            Users(
            name = data['name'],
            email = data['email'],
            password = data['password']
            ).save()
        return JsonResponse({'message':'SUCCESS'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['user']
        password = data['password']
        
        if Users.objects.filter(name=username).exists():
            user = Users.objects.get(name=username)
        elif Users.objects.filter(email=username).exists():
            user = Users.objects.get(email=username)
        
        if user.password == password:
            return JsonResponse({'message':'SUCCESS'}, status=200)
        else:
            return JsonResponse({"message":'WRONG_PASSWORD'}, status=401)


