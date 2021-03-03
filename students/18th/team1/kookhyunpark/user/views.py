import json

from django.http  import JsonResponse, request
from django.views import View

from user.models import User

class SignUpView(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            #email = data['email']
            #phone = data['phone'].replace('-','')
            #user_name     = data['user_name']
            #password = data['password']

            if not data['email'] or not data['password']:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            elif '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message':'EMAIL VALIDATION ERROR'}, status=400)
            elif len(data['password']) < 8:
                return JsonResponse({'message':'PASSWORD VALIDATION ERROR'}, status=400)
            elif User.objects.filter(email=data['email']).exists() or User.objects.filter(phone=data['phone']).exists() or User.objects.filter(user_name=data['user_name']).exists():
                return JsonResponse({'message':'USER ALREADY EXISTS'}, status=400)


            user = User.objects.create(
                email         = data['email'],
                phone         = data['phone'].replace('-',''),
                full_name     = data['full_name'],
                user_name     = data['user_name'],
                password      = data['password'],
                date_of_birth = data['date_of_birth'],
            )
            return JsonResponse({'message':'SUCCESS'}, status=202)        
        #except KeyError:
        #    return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message": "VIEW ERROR"}, status=400)

        #return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
