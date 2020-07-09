import json
from django.views import View
from django.http import JsonResponse
from .models import User

class signUp(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            if (data['email'] in '@') and (len(data['password']) > 5):

                User(
                        name = data['name'],
                        email = data['email'],
                        password = data['password']
                        ).save()

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            
            else:
                return JsonResponse({'message':'INVAILD_FORMAT'}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)


    def get(self, request):
        user_data = user.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)

class signIn(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            if User.objects.get(name=data['name']) and User.objects.get(password=data['password']):
                return JsonResponse({'message':'SUCCESS'}, status=200)

        except User.DoesNotExist:

            return JsonResponse({"message": "INVALID_USER"}, status=401)
