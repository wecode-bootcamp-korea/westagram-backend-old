import json

from django.http  import JsonResponse
from django.views import View

from .models      import User


class RegisterView(View):
    def post(self,request):

        try:
            MIN_EMAIL_LENGTH = 8
            data             = json.loads(request.body)
            name             = data['name']
            phonenumber      = data['phonenumber'].replace("-",'')
            email            = data['email']
            password         = data['password']
            nickname         = data['nickname']
            
            if email.find("@") == -1 or email.find(".") == -1:
                return JsonResponse({'MESSAGE :':"INVAILD EMAIL ADDRESS!"},status = 400)
            
            if len(password)<MIN_EMAIL_LENGTH:
                return JsonResponse({'MESSAGE :':"PASSWORD TOO SHORT!"},status = 400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE :':"EMAIL ALREADY EXISTS!"},status = 400)

            if User.objects.filter(phonenumber=phonenumber).exists():
                return JsonResponse({'MESSAGE :':"PHONENUMBER ALREADY EXISTS!"},status = 400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE :':"NICKNAME ALREADY EXISTS!"},status = 400)
            
            User.objects.create(
                name        = name,
                phonenumber = phonenumber, 
                email       = email, 
                password    = password,
                nickname    = nickname
            )
            
            return JsonResponse({'MESSAGE :':"SUCCESS "},status = 200)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except BlankFieldException as e:
            return JsonResponse({'MESSAGE :':e.__str__()},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)


class LoginView(View):
    def post(self,request):

        try:
            data             = json.loads(request.body)
            email            = data['email']
            password         = data['password']
            user_info        = User.objects.get(email=email)

            if user_info.password == password:
                return JsonResponse({'MESSAGE :':"SUCCESS"}, status = 200)
            else:
                return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)
        
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except IndexError:
            return JsonResponse({'MESSAGE :':"INDEX_ERROR"},status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)

