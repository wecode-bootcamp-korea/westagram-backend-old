import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError, IntegrityError
from django.db.models import Q

from posting.models   import Post
from user.models      import User

class PostView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email        = data.get('email')
            phone_number = data.get('phone_number')
            account      = data.get('account')
            image_url = data['image_url']

            user = User.objects.get(email=email)
            Post.objects.create(user=user, image_url=image_url)
            # if User.objects.filter(Q(email=email)|Q(phone_number=phone_number)|Q(account=account)).exists():
            #     User.objects.create(email=email, password=encrypted_password, phone_number=phone_number, account=account)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=400)        

class ShowView(View):
    def get(self, request):
        try:
            data         = json.loads(request.body)
            email        = data.get('email')
            phone_number = data.get('phone_number')
            account      = data.get('account')
            password     = data['password']
            user_account = [email, phone_number, account]

            if not (email or account or phone_number):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if User.objects.filter(Q(email=email)|Q(phone_number=phone_number)|Q(account=account)).exists():
                user = User.objects.get(Q(email=email)|Q(phone_number=phone_number)|Q(account=account))

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    user_id = user.id
                    access_token = jwt.encode({'user_id': user_id}, SECRET, algorithm='HS256')
                    return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)
                else:
                    return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            return JsonResponse({'message':'INVALID_USER'}, status=401)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)