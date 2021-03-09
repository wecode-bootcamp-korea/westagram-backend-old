import re, json, bcrypt

from django.views                 import View
from django.http                  import JsonResponse, request
from django.db.models.query_utils import Q
from json.decoder                 import JSONDecodeError

from user.utils  import LoginCheck
from user.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email         = data['email']
            password      = data['password']
            phone         = data.get('phone', None)
            full_name     = data.get('full_name', None)
            user_name     = data.get('user_name', None)
            date_of_birth = data.get('date_of_birth', None)

            if phone:
                phone = phone.replace('-','')

            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '\S{8,20}'

            if not re.match(REGEX_EMAIL,email):
                return JsonResponse({'message':'EMAIL VALIDATION ERROR'}, status=400)
            if not re.match(REGEX_PASSWORD,password):
                return JsonResponse({'message':'PASSWORD VALIDATION ERROR'}, status=400)

            if not User.objects.filter(email=email):
                if phone and User.objects.filter(phone=phone):
                    return JsonResponse({'message':'PHONE ALREADY EXISTS'}, status=400)
                elif user_name and User.objects.filter(user_name=user_name):
                    return JsonResponse({'message':'USER_NAME ALREADY EXISTS'}, status=400)
            else:
                return JsonResponse({'message':'EMAIL ALREADY EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                email         = email,
                phone         = phone,
                full_name     = full_name,
                user_name     = user_name,
                password      = hashed_password,
                date_of_birth = date_of_birth,
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)     

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except Exception as e:
            print(e)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id  = data['user_id']
            password = data['password']

            user= User.objects.get(Q(user_name=user_id)|Q(email=user_id)|Q(phone=user_id))

            if user:
                stored_password  = User.objects.get(Q(user_name=user_id)|Q(email=user_id)|Q(phone=user_id)).password
                if not bcrypt.checkpw(password.encode('UTF-8'), stored_password.encode('UTF-8')):
                    return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)                
            else:
                return JsonResponse({"message":"INVALID_USER"}, status=401)   
            
            return JsonResponse({"message":"SUCCESS", "Authorization":LoginCheck(user.id)}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON DECODE ERROR'}, status=400)
        except Exception as e:
            print(e)