import json
from django.views import View
from django.http  import JsonResponse
from user.models  import User

class CreateUser(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            email    = data['email'],
            name     = data['name'],
            nickname = data['nickname'],
            password = data['password'],
        )
        if not (data['email'] and data['name'] and data['nickname'] and data['password']):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        if User.objects.filter(email = data['email']).exists():
            return JsonResponse({'message':'EXIST_ID'}, status = 400)
        if User.objects.filter(nickname = data['nickname']).exists():
            return JsonResponse({'message':'EXIST_NICKNAME'}, status = 400)
        if len(data['password']) < 8:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        else:
            User.objects.create(
                email    = data['email'], 
                name     = data['name'], 
                nickname = data['nickname'], 
                password = data['password']
            )
            return JsonResponse({'message':'SUCCESS'}, status = 200)
    



