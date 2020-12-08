import jwt
from functools import wraps

from django.http            import JsonResponse

from westargram.my_settings import SECRET_KEY, encryption_algorithm
from user.models            import User


def login_required(func):
    @wraps(func)
    def decorated_function(self, request, *args, **kwargs):
        try:
            request_headers = request.headers
            token           = request_headers['Authorization']
            decoded_token   = jwt.decode(token, SECRET_KEY, algorithms=encryption_algorithm)
            user_id         = decoded_token['user_id']
            user            = User.objects.get(id=user_id) if user_id else None
            request.user_id = user_id
            request.user    = user
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'USER DOES NOT EXIST'}, status=401)
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({'MESSAGE': 'AUTHORIZATION FAIL: INVALID_TOKEN'}, status=401)
        return func(self, request, *args, **kwargs)
    return decorated_function
