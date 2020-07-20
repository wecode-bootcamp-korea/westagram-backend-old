import json, jwt

from django.http        import JsonResponse

from .models            import User
from westagram.settings import SECRET_KEY, ALGORITHM

class LoginConfirm:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
                user = User.objects.get(id = payload['user'])
                request.user = user
                return self.func(self, request, *args, **kwargs)
            return JsonResponse({'message': 'NEED_LOGIN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)

        except jwt.DecodeError:
            return JsonRespose({'message': 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
