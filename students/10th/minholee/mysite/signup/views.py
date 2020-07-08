from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Users
import json

# Create your views here.

class Signup(View):
    def post(self, request):
        try:
            bring_data = json.loads(request.body)
            Users(
                    name     = bring_data['name'],
                    email    = bring_data['email'],
                    password = bring_data['password']
            ).save()
            return JsonResponse({"Message":"SUCCESS"}, status=200)
            
        except KeyError: 
            return JsonResponse({"Message":"KEY_ERROR"}, status=400)

    def get(self, request):
        db_data = Users.objects.values()
        return JsonResponse({"Users List":list(db_data)}, status=200)


class Signin(View):
    def post(self, request):
        bring_data = json.loads(request.body)
        try:
            #if Users.objects.get(email=bring_data['email']).email == bring_data['email']:
            if bring_data['email'] in Users.objects.get(email=bring_data['email']).email:
                user = Users.objects.get(email=bring_data['email'])
                if user.password == bring_data['password']:
                    return JsonResponse({"Message":"SUCCESS"}, status=200)
                else:
                    return JsonResponse({"Message":"PASSWORD_ERROR"}, status=201)
        except Exception as e:
                return JsonResponse({"Message":f"{e}"}, status=401)
