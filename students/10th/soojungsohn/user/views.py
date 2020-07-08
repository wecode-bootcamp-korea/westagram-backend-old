import json

from django.views   import View 
from django.http    import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            new_name        = data['name']
            new_email       = data['email']
            new_password    = data['password']
            
            if User.objects.filter(name=new_name).exists():
                return JsonResponse({'message':'EXISTING_ACCOUNT'}, status=401)
            else:
                if ('@' in new_email) and (len(new_password)>=5) : 
                    User(
                        name        = new_name,
                        email       = new_email,
                        password    = new_password
                    ).save()
                    return JsonResponse({'message' : 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message' : 'VALIDATION_ERROR'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username = data['user']
            password = data['password']
            
            if User.objects.filter(name=username).exists():
                user = User.objects.get(name=username)
            elif User.objects.filter(email=username).exists():
                user = User.objects.get(email=username)
        
            if user.password == password:
                return JsonResponse({'message' : 'SUCCESS'}, status=200)
            else:
                return JsonResponse({"message":'UNAUTHORIZED'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

