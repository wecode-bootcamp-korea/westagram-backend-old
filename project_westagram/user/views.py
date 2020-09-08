import json
from django.views import View
from django.http  import JsonResponse
from .models      import User

class SignUp(View):
  def post(self, request):
    data = json.loads(request.body)

    UserData = User(
    phoneNumber = data['phoneNumber'],
    name        = data['name'],
    email       = data['email'],
    password    = data['password'],
    )

    if UserData.email is False or UserData.password is False:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    if ('@' and '.') not in UserData.email:
      return JsonResponse({'message' : 'email invalidation!'}, status = 400)

    if len(UserData.password) < 8:

      return JsonResponse({'message' : 'PW invalidation!'}, status = 400)


    if User.objects.filter(phoneNumber=UserData.phoneNumber).exists():
      return JsonResponse({'message' : 'phoneNumber exists!'}, status = 400)
    elif User.objects.filter(name=UserData.name).exists():
      return JsonResponse({'message' : 'Name exists!'}, status = 400)
    elif User.objects.filter(email=UserData.email).exists():
      return JsonResponse({'message' : 'Email exists!'}, status = 400)

    UserData.save()
    return JsonResponse({'message' : 'SUCCESS'}, status = 200)

  def get(self, request):
    user_data = User.objects.values()
    return JsonResponse({'USERS':list(user_data)}, status = 200)

class LoginView(View):
  def post(self, request):
    data = json.loads(request.body)

    UserData = User(
    phoneNumber = data['phoneNumber'],
    name        = data['name'],
    email       = data['email'],
    password    = data['password'],
    )

    savedData = User.objects.get(name=UserData.name)
    # 1. 로그인할 땐 전화번호, 사용자 이름 또는 이메일이 필수, 비밀번호도 있어야 함.
    if not UserData.password or not UserData.phoneNumber:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    # 2. 계정이 존재하지 않을 때나 비밀번호가 맞지 않을 때, invalid_user, 401
    if (savedData.email != UserData.email) or (savedData.password != UserData.password):
      return JsonResponse({'message' : 'INVALID_USER'}, status=401)

    return JsonResponse({'message':'SUCCESS'}, status=200) 
