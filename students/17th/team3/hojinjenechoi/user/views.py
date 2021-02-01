import json

from django.views           import View
from django.http            import JsonResponse 

from user.models  import User

class SignUpView(View):
    def post(self, request):

        signup_data = json.loads(request.body)

        try:
            if signup_data['email'] == '' or signup_data['password'] == '':
                return JsonResponse({'message':'PLEASE ENTER YOUR EMAIL OR PASSWORD'}, status=400)

            if '@' not in signup_data['email'] or '.' not in signup_data['email']:
              return JsonResponse({'message':'EMAIL INVALIDATION.'}, status=400)

            if User.objects.filter(email=signup_data['email']).exists() or User.objects.filter(phone=signup_data['phone']).exists():
                return JsonResponse({'message':'USER ALREADY EXISTS.'}, status=409)
            
            if User.objects.filter(nickname=signup_data['nickname']).exists():
                return JsonResponse({'message':'NICKNAME ALREADY EXISTS.'}, status=409)

            if len(signup_data['password']) < 8:
                return JsonResponse({'message':'PASSWORD SHOULD BE LONGER THAN 8 LETTERS.'}, status=400)
            
            
            signup_user = User.objects.create(
                email    = signup_data['email'],
                password = signup_data['password'],
                nickname = signup_data['nickname'],
                phone   = signup_data['phone']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError: 
            return JsonResponse({'message':'KEY ERROR'}, status=400)

        except BlankFieldException as e:
            return JsonResponse({'message':e.__str__()}, status=400)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'message':list(user)}, status=200)