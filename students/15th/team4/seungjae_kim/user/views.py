import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse, HttpResponse
from django.views import View
from user.models  import Users
from my_settings  import SECRET_KEY

from user.utils   import LoginConfirm, is_valid

class SignupView(View):    

    def post(self,request):
        
        PW_REGEX    = '^[A-Za-z0-9@#$%^&+=]{8,}$'
        EMAIL_REGEX = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
     
        data = json.loads(request.body)
        
        try:
            assert is_valid(data['email'],EMAIL_REGEX), "INVALID_EMAIL_FORMAT"
            assert is_valid(data['password'],PW_REGEX), "INVALID_PW_FORMAT"

            hased_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            

            if Users.objects.filter(email = data['email']).exists(): 
                return JsonResponse({"MESSAGE" : "USER_ALREADY_EXISTS"},status=400)
                
            Users.objects.create(email = data["email"],password=hased_password.decode())   
            return JsonResponse({"MESSAGE" : "SUCCESS"},status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"},status=400)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE": f"{e}"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)


class SigninView(View):

    def post(self, request):

        data = json.loads(request.body)

        try:
            user = Users.objects.get(email = data['email'])
            
            assert bcrypt.checkpw(data['password'].encode(), user.password.encode())
            
            access_token = jwt.encode({"id":user.id}, SECRET_KEY, algorithm='HS256')
            
            return JsonResponse({'MESSAGE': "SUCCESS","TOKEN": access_token.decode()},status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"},status=400)

        except (Users.DoesNotExist, AssertionError):
            return JsonResponse({'MESSAGE': "INVALID_USER"},status=401)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)

class FollowsView(View):
    
    @LoginConfirm
    def post(self, request, user_pk):

        try:
            followed = Users.objects.get(id=user_pk)
            
            if not request.user in followed.following.all():
                followed.following.add(request.user)

                return JsonResponse({"MESSAGE":"SUCCESS"},status=201)
            else:
                return JsonResponse({"MESSAGE":"ALREADY_FOLLOWING"},status=400)
            
        except Users.DoesNotExist:
            return JsonResponse({"MESSAGE":"USER_NOT_FOUND"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)
    
    @LoginConfirm
    def delete(self, request, user_pk):

        try:
            followed = User.objects.get(id=user_pk)

            if not request.user in followed.following.all():
                followed.following.add(request.user)

                return JsonResponse({"MESSAGE":"SUCCESS"},status=201)
            else:
                return JsonResponse({"MESSAGE":"DID U REALLY FOLLOWED HIM/HER?"},status=404)

        except Users.DoesNotExist:
            return JsonResponse({"MESSAGE":"USER_NOT_FOUND"},status=400)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)
