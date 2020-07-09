from django.shortcuts import render
import json
from django.views import View
from django.http  import JsonResponse
from .models      import Users, Comment_Data


class MainView(View):
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
        try:
            if Users.objects.filter(email = data['email']).exists():
                user = Users.objects.get(email = data['email'])
            else:
                return JsonResponse({'message':'get wrong'}, status = 401)

            if user.password == data['password']:
                return JsonResponse({'message':'SUCCESS'}, status=200)
            return JsonResponse({'message':'get wrong'}, status = 401)
        except KeyError:
            return JsonResponse({'message':'key wrong'}, status=400)

class Comment(View):
    def post(self, request):
        data = json.loads(request.body)
        Comment_Data(
            name_co = data['name_co'],
            text_co = data['text_co']
        ).save()
        Co = Comment_Data.objects.values()
        return JsonResponse({'comment':list(Co)}, status=200)
    
    def get(self, request):
            Co = Comment_Data.objects.values()
            return JsonResponse({'comment':list(Co)}, status=200)
        
      

        # Create your views here.
