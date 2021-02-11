import json
from django.views import View
from django.http  import JsonResponse
from .models      import User
import bcrypt
import jwt


class SignUp(View):
  def post(self, request):
    PASSWORD_LENGTH_LIMIT = 8
    try:
      data = json.loads(request.body)
    except ValueError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


    if User.objects.filter(phoneNumber=data['phoneNumber']) or User.objects.filter(email=data['email']) or User.objects.filter(name=data['name']):
      return JsonResponse({'message' : 'ALREADY_EXIST'}, status=400)
    else:
      if '@' not in data['email'] or '.' not in data['email']:
        return JsonResponse({'message' : 'email invalidation!'}, status = 400)
      if len(data['password']) <= PASSWORD_LENGTH_LIMIT:
        return JsonResponse({'message' : 'PW invalidation!'}, status = 400)

    user_data = User(
    phoneNumber = data['phoneNumber'],
    name        = data['name'],
    email       = data['email'],
    password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    ).save()

    return JsonResponse({'message' : 'SUCCESS'}, status = 200)

  def get(self, request):
    user_data = User.objects.values()
    return JsonResponse({'USERS':list(user_data)}, status = 200)

class LoginView(View):
  def post(self, request):
    try :
      payload = json.loads(request.body)
      
    except ValueError:
      return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
    
    savedData = User.objects.get(email=payload['email'])
    if not (savedData and bcrypt.checkpw(payload['password'].encode(), savedData.password.encode())):
      return JsonResponse({'message' : 'INVALID_USER'}, status=401)

    login_token = jwt.encode({'user_id' : savedData.id} , 'secret_key', algorithm = 'HS256').decode() ## string형태의 hashed_pw가 token화 되어서 byte화 되어 나옴.
    return JsonResponse({'access_token':login_token}, status=200)