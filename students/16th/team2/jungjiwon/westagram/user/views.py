import json
from django.http    import JsonResponse
from django.views   import View
from user.models    import User

class UsersView(View):
    def post(self, request):   
        data = json.loads(request.body)
        signup_db = User.objects.all()
        user=User(
        account     = data['account'],
        password    = data['password'],
        email       = data['email'],
        tel_num     = data['tel_num'],
        )

        try:
            
            if signup_db.filter(account = data['account']).exists():
                return JsonResponse({'MESSAGE':'EXISTING ID'}, status=400)
            if signup_db.filter(email = data['email']).exists():
                return  JsonResponse({'MESSAGE':'EXISTING MAIL'}, status=400)
            if signup_db.filter(tel_num = data['tel_num']).exists():
                return  JsonResponse({'MESSAGE':'EXISTING NUMBER'}, status=400)
            if len(data['password']) < 8:
                return JsonResponse({'MESSAGE':'PASSWORD TOO SHORT'}, status=400)
            if '@' or '.' not in data['email']:
                return JsonResponse({'MESSAGE':'INVALID EMAIL'}, status=400)
            
            user.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self, request):
        data        = json.loads(request.body)
        signup_db   = User.objects.all()
        

        try:
            if signup_db.filter(account = data['login_account']).exists():
                login = User.objects.get(account = data['login_account'])
            if signup_db.filter(email = data['login_account']).exists():
                login = User.objects.get(email = data['login_account'])
            if signup_db.filter(tel_num = data['login_account']).exists():
                login = User.objects.get(tel_num = data['login_account'])
        
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        print(login.password)
        if login.password == data['password']:
            return JsonResponse({'MESSAGE':'LOGIN SUCCESS'}, status=200)
        if login.password != data['password']:
            return JsonResponse({'MESSAGE':'Invalid Password'}, status=400)