import json, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models       import Q

from .models      import User

class UserSignup(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            username  = data['username']
            phone_num = data['phone_num']

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
            return JsonResponse({"message":"VAlue_ERROR"}, status=400)
        
class UserSignin(View):
    def post(self, request):
        try:
            users     = User.objects.all()
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']
            username  = data['username']
            phone_num = data['phone_num']
        except KeyError:
            print("==========================")
            print(email, password)
            print("==========================")
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message":"VAlue_ERROR"}, status=400)
        
        except User.ObjectDoesNotExist:
            return JsonResponse({"message":"INVALID_USER"}, status=401) 


        # temps = User.objects.filter(username=username) | User.objects.filter(email=email) | User.objects.filter(phone_num=phone_num) | User.objects.filter(password=password)

        if not password or not email:
            print("**************************")
            print(email, password)
            print("**************************")

            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        elif email == '' and username == '' and phone_num == '':
            print("--------------------------")
            print(email, password)
            print("--------------------------")
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        
        user=User.objects.filter(Q(username=username) | Q(email=email) | Q(phone_num=phone_num))
        print(user)
        user=user.get()
        print("8888888888888888888888888888888")
        print(user)
        print("8888888888888888888888888888888")
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return JsonResponse({'result': 'SUCCESS'}, status=200)
        # else:
        #     for temp in temps:
        #         if username == temp.username or email == temp.email or phone_num == temp.phone_num:
        #             if password == temp.password:
        #                 return JsonResponse({'result': 'SUCCESS'}, status=200)
        #     return JsonResponse({"message":"INVALID_USER"}, status=401) 


