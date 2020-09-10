import json
import jwt
import bcrypt

from django.http  import JsonResponse
from django.views import View

from .models      import Users
from project_westagram.settings import SECRET_KEY

class SignUp(View):
  def post(self,request):
    data = json.loads(request.body)
   
    if '@' and '.' not in data['email']:
      return JsonResponse({'message':'no email error'},status=404)  
    elif len(data['password']) < 8:
      return JsonResponse({'message':'short length error'},status=404)
    elif (data['email'] and data['password']) == False:
      return JsonResponse({'message':'key error'},status=404)      

    Users(
      email        = data['email'],
      password     = data['password'],
    ).save()

    return JsonResponse({'message':'SUCCESS'},status=200)

  def get(self,request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)

class SignIn(View):
  def post(self,request):
    data = json.loads(request.body)

    if (data['email'] and data['password']) == False:
      return JsonResponse({'message':'key error'},status=404)
    elif (Users.objects.filter(password=data['password']).exists() or
      Users.objects.filter(email=data['email']).exists())==False:
      return JsonResponse({'message':'invalid_user'})

    email = Users.objects.get(email = data['email']
    password = data['password']
    access_token = jwt.encode({'email' : email}, SECRET, algorithm = 'HS256')


    return JsonResponse({'access_token': access_token}, status=200)

  def get(self,request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)
