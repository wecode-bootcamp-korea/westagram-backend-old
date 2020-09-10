import json

from django.http  import JsonResponse
from django.views import View

from .models      import Users

class SignUp(View):
  def post(self,request):
    data = json.loads(request.body)
   
    if '@' and '.' not in data['email']:
      return JsonResponse({'message':'ERROR1'},status=404)  
    elif len(data['password']) < 8:
      return JsonResponse({'message':'ERROR2'},status=404)
    elif (data['email'] and data['password']) == False:
      return JsonResponse({'message':'key error'},status=404)      

    Users(
      email        = data['email'],
      name         = data['name'],
      password     = data['password'],
      phone_number = data['phone_number']
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
    elif (Users.objects.filter(name=data['name']).exists() or
      Users.objects.filter(email=data['email']).exists())==False:
      return JsonResponse({'message':'invalid user'},status=404)
    return JsonResponse({'message':'success'},status=200)

  def get(self,request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)
