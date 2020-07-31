import json

from django.views import View
from django.http import JsonResponse

from .models import Users, Comments
# Create your views here.

class MainView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            Users(
                name = data['name'],
                email = data['email'],
                password = data['password']
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)}, status=200)

class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        if Users.objects.filter(email=data['email']).exists():
            user = Users.objects.get(email=data['email'])
            if data['password'] == user.password:
                return JsonResponse({'message':'SUCCESS'}, status=200)
            return JsonResponse({'message':'INVALID_USER'}, status=400)

class Comment(View):
    def post(self, request):
        data = json.loads(request.body)
        Comments(
            name = data['name'],
            comment  = data['comment']
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)

    def get(self, request):
        user_data = Comments.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)
