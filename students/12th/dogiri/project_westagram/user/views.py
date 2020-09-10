import json

from django.http  import JsonResponse
from django.views import View

from .models      import Users

class SignUp(View):
  def post(self,request):
    data = json.loads(request.body)
   
    if '@' and '.' not in data['email']
      return JsonResponse({'message':'ERROR1'}  
    elif len(data['password'] < 8
      return JsonResponse({'message':'ERROR2'}
    elif (Users.object.filter(name=data['name']).exist()

    Users(
      email        = data['email']
      name         = data['name']
      password     = data['password']
      phone_number = data['phone_number']
    ).save()

    return JsonResponse({'message':'SUCCESS'},status=200)

  def get(self.request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)
