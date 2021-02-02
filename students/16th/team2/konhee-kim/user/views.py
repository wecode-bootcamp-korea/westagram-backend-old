import json

from django.http  import JsonResponse
from django.views import View

from user.models  import User
from user import utils

class SignUpView(View):

    def post(self, request):
        try:
            data      = json.loads(request.body)

            email     = data['email']
            mobile    = data['mobile']
            username  = data['username']
            full_name = data['full_name']
            password  = data['password']
            mobile = ''.join(mobile.split('-'))
           
            # validation checking
            if not utils.validate_email(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
            
            if not utils.validate_password(password):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
            
            if mobile and not(utils.validate_mobile(mobile)):
                return JsonResponse({'MESSAGE': 'INVALID_MOBILE'}, status=400)
            
            if not username:
                return JsonResponse({'MESSAGE': 'BLANK_USERNAME'}, status=400)
            
            mobile = ''.join(mobile.split('-'))
            
            # existence check
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
            
            if User.objects.filter(username = username).exists():
                return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)
            
            if mobile and User.objects.filter(mobile_number = mobile).exists():
                return JsonResponse({'MESSAGE': 'EXISTENCE_ERROR'}, status=400)

            # create user account
            created_user = User.objects.create(
                email         = email,
                mobile_number = mobile,
                full_name     = full_name,
                username      = username,
                password      = utils.hash_password(password)
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LogInView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)

            email    = data['email']
            password = data['password']
            
            # validation checking
            if not utils.validate_email(email):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
            
            if not password:
                return JsonResponse({'MESSAGE': 'BLANK_PASSWORD'}, status=400)

            # log-in process
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)

            hashed_password = User.objects.get(email=email).password 
            
            if utils.check_password(password, hashed_password):
                loged_in_user = User.objects.get(email=email)
                user_id       = loged_in_user.id
                access_token  = utils.generate_access_token(user_id)
                
                return JsonResponse({'MESSAGE'     : 'SUCCESS',
                                     'ACCESS_TOKEN': access_token}, status=200)

            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
