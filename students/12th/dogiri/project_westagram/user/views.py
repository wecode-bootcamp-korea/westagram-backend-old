import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from .models      import Users
from project_westagram.settings import SECRET_KEY

class SignUp(View):
  def post(self,request):
    data = json.loads(request.body)
   
    if '@' and '.' not in data['email']:
      return JsonResponse({'message':'NOT EMAIL FORM'},status=404)  
    elif len(data['password']) < 8:
      return JsonResponse({'message':'SHORT LENGTH'},status=404)
    elif (data['email'] and data['password']) == False:
      return JsonResponse({'message':'KEY ERROR'},status=404)      

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    Users(
      email        = data['email'],
      password     = hashed_password.decode('utf-8'),
    ).save()

    return JsonResponse({'message':'SUCCESS'},status=200)

  def get(self,request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)

class SignIn(View):
  def post(self,request):
    data = json.loads(request.body)

    if data['email'] == False:
      return JsonResponse({'message':'KEY ERROR'},status=404)
    elif Users.objects.filter(email=data['email']).exists()==False:
      return JsonResponse({'message':'INVALID USER'})
   
    hash_password = Users.objects.get(email=data['email'])
    hash_password2 = hash_password.password
    check_password = data['password']    
    signin_user = Users.objects.get(email=data['email'])

    if bcrypt.checkpw(check_password.encode('utf-8'),hash_password2.encode('utf-8'))==True:
      token = jwt.encode({'user_id' : signin_user.id,},SECRET_KEY,algorithm = 'HS256').decode('utf-8')
      return JsonResponse({'Authorization':token},status=200)
    else:
      return JsonResponse({'message':'INVALIE PASSOWRD'})

  def get(self,request):
    user_data = Users.objects.values()
    return JsonResponse({'users':list(user_data)},status=200)
