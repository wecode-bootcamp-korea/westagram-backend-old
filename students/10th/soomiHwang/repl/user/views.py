import json

from django.views import View
from django.http  import JsonResponse

from .models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        try: 
            if Users.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status=401)
            else: 
                Users.objects.create(
                    name     = data['name'],
                    email    = data['email'],
                    password = data['password']
                ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'}, status=400)

    def get(self, request):
      user_data = Users.objects.values()
      return JsonResponse({'users':list(user_data)}, status=200)


class SignIn(View): 
    def get(self, request):
        data = json.loads(request.body)
        try:
            if data['email'] in Users.objects.filter(email = data['email'])[0].email:
                user = Users.objects.get(email=data['email'])
                if user.password==data['password']:
                    return JsonResponse({'Message':'Success!'}, status=200)
                else:
                    return JsonResponse({'Message':'Password error'}, status=404)

        except KeyError:
            return JsonResponse({'Message':'Key_error'}, status=400)
    

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)


