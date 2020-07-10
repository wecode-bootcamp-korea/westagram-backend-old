import json
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        Users(
              name     = data['name'],
              email    = data['email'],
              password = data['password']
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)

    def get(self, request):
       user_data = Users.objects.values()
       return JsonResponse({'users':list(user_data)}, status=200)


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        print('exists 없을 때', Users.objects.filter(email=data['email']))
        print('exists 있을 때',Users.objects.filter(email=data['email']).exists())


        if Users.objects.filter(email=data['email']):
            i = Users.objects.get(email=data['email'])
            if i.password == data['password']:
                    return JsonResponse({'message':f'{i.email}회원님 로그인 성공'}, status=200)
            else:
                    return JsonResponse({'message':'비밀번호 오류'}, status=401)

        return JsonResponse({'message':'INVALID_USER'}, status=400)

  #  def get(self, request):
  #      user_data = Users.objects.values()
  #      return JsonResponse({'users':list(user_data)}, status=200)


