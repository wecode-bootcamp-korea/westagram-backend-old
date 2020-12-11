import json, jwt
from user.models import User
from my_settings import SECRET_KEY, ALGORITHM
from django.http import JsonResponse

class LoginConfirm:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user = User.objects.get(id=token_payload['user-id'])
                request.user = user
                return self.original_function(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE' : 'NEED_LOGIN'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE' : 'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)

