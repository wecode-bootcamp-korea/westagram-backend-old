import json, bcrypt, jwt, re

from django.http     import JsonResponse
from django.views    import View
from django.db.utils import DataError, IntegrityError

from user.models     import User

PASSWORD_MINIMUM_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = str(data['email'])
            password = str(data['password'])

            if "" in (email, password):
                return JsonResponse({'message':'NO_VALUE_ERROR'}, status=400)
            
            email_regex = re.compile("^.+@+.+\.+.+$")
            
            if not email_regex.match(email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)

            if len(password) < PASSWORD_MINIMUM_LENGTH:
                return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)

            encoded_password = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(encoded_password, salt)
            encrypted_password = hashed_password.decode('utf-8')
            
            user = User.objects.create(email=email, password=encrypted_password)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=200)