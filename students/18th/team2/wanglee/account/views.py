import json, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q

from .models      import User
from my_settings  import SECRET_KEY

class UserSignup(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data.get('email')
            password  = data.get('password')
            username  = data.get('username')
            phone_num = data.get('phone_num')

            if ('@' and '.') not in email:
                return JsonResponse({"message":"email must contain the '@' symbol and the period'.'"}, status=400)
            
            if len(password) < 8:
                return JsonResponse({"message":"password must be at least 8 characters"}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message":"That username is taken. Try another"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"That email is taken. Try another"}, status=400)

            if User.objects.filter(phone_num=phone_num).exists():
                return JsonResponse({"message":"That phone number is taken. Try another"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            User.objects.create(username=username, email=email, password=hashed_password.decode('utf-8'), phone_num=phone_num)
            return JsonResponse({'result': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message":"Value_ERROR"}, status=400)
        
class UserSignin(View):
    def post(self, request):
        try:
            users     = User.objects.all()
            data      = json.loads(request.body)
            email     = data.get('email')
            password  = data.get('password')
            username  = data.get('username')
            phone_num = data.get('phone_num')

            user=User.objects.get(Q(email=email) | Q(username=username) | Q(phone_num=phone_num))

            if email == None and username == None and phone_num == None:
                return JsonResponse({"message":"KEY_ERROR"}, status=400)
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'pk':user.pk, 'username':username, 'email':email, 'phone_num':phone_num}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'token': token, 'result': 'SUCCESS'}, status=200)

            return JsonResponse({"message":"INVALID_USER"}, status=401) 

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message":"VAlue_ERROR"}, status=400)