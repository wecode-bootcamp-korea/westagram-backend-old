import json
import jwt
import my_settings

from json.decoder import JSONDecodeError
from jwt import DecodeError
from jwt import InvalidSignatureError
from posting.models import Posting
from user.models import User

from django.http import JsonResponse

SECRET_KEY = my_settings.SECRET_KEY['secret']

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ACCESS_TOKEN = data['ACCESS_TOKEN']
            payload = jwt.decode(ACCESS_TOKEN, SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            request.user = user
            return func(self, request, *args, **kwargs)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)

        except DecodeError:
            return JsonResponse({'message': 'INVALID_ACCESS_TOKEN'}, status=401)

        except InvalidSignatureError:
            return JsonResponse({'message': 'INVALID_ACCESS_TOKEN'}, status=401)

    return wrapper