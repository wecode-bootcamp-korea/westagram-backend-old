import json

from django.views import View
from django.http  import JsonResponse

from .models      import Users


class Signup(View):
    def post(self, request):
        data = json.loads(request.body)
        signup_db = Users.objects.all()
        try:
            user_id     = data['user_id']
            email       = data['email']
            password    = data['password']
            phonenumber = data['phonenumber']
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if user_id != '':
            if signup_db.filter(user_id = data['user_id']).exists() :
                return JsonResponse({'message':'ID : already exists'}, status=400)
        if email != '':
            if signup_db.filter(email = data['email']).exists():
                return JsonResponse({'message':'email : already exists'}, status=400)
            elif '@' not in email or '.' not in email :
                return JsonResponse({'message':'email needs @ and .(dot)'}, status=400)
        if len(password) < 8 :
                return JsonResponse({'message':'The length of password should be more than 8'}, status=400)
        if phonenumber != '':
            if signup_db.filter(phonenumber = data['phonenumber']).exists():
                return JsonResponse({'message':'phonenumber : already exists'}, status=400)     
        
        Users(
              user_id     = data['user_id'],
              email       = data['email'],
			  password    = data['password'],
              phonenumber = data['phonenumber']
                 ).save()
        return JsonResponse({'message':'SUCCESS'}, status=200)
           
    def get(self, request):
            user_data = Users.objects.values()
            return JsonResponse({'This is Newbie\'s data':list(user_data)}, status=200)


# User.objects.filter(name = data['name'], email= data['email'], password = data['password']).exists()


