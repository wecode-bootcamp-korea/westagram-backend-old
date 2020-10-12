# autopep8: off
import os
import jwt
import json

from pathlib                import Path
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from auth.models            import Users

BASE_DIR = Path(__file__).resolve().parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as file:
    secrets = json.loads(file.read())


def get_secret(key, secrets=secrets):
    try:
        return secrets[key]
    except KeyError:
        raise ImproperlyConfigured('check secrets.json')


def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token     = request.headers.get('Auth', None)
            key       = get_secret('JWT_KEY')
            algorithm = get_secret('JWT_ALGORITHM')

            if token:
                decode       = jwt.decode(token, key, algorithm=algorithm)
                user         = Users.objects.get(id=decode['user'])
                request.user = user
        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=403)
        except Users.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=403)

        return func(self, request, *args, **kwargs)

    return wrapper
