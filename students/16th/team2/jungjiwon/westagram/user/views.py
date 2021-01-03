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
                return JsonResponse({'MESSAGE':'existing ID'}, status=400)
            if signup_db.filter(email = data['email']).exists():
                return  JsonResponse({'MESSAGE':'existing email'}, status=400)
            if signup_db.filter(tel_num = data['tel_num']).exists():
                return  JsonResponse({'MESSAGE':'existing number'}, status=400)
            if len(data['password']) < 8:
                return JsonResponse({'MESSAGE':'password too short'}, status=400)
            if '@' and '.' not in data['email']:
                return JsonResponse({'MESSAGE':'Invailid Email'}, status=400)
            
            user.save()
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
