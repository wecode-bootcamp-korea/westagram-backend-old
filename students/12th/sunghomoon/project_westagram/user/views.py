import json
from django.views import View
from django.http  import JsonResponse
from .models      import User

class SignView(View):
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

    # 1. 로그인할 땐 전화번호, 사용자 이름 또는 이메일이 필수, 비밀번호도 있어야 함.
    if UserData.password is False or UserData.phoneNumber is False:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    # 2. 계정이나 패스워드가 전달되지 않으면, keyerror, 400
    if not(UserData.name and UserData.email) or not UserData.password:
      return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    savedData = User.objects.filter(phoneNumber=UserData.phoneNumber)


    # 4. 로그인 성공 시 Success, 200
    return JsonResponse({'message': 'SUCCESS'}, status=200)
