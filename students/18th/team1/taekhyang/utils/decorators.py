import jwt
import json
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from account.models             import User
from project_westagram.settings import SECRET_KEY
from utils.debugger             import debugger


def auth_check(func):
    def wrapper(self, request):
        data = request.headers
        try:
            token = data.get('Authorization')
            if not token:
                return JsonResponse({'message': 'TOKEN_DOSE_NOT_EXIST'})
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            
            user_id = decoded_auth_token['user_id']
            user    = User.objects.get(id=user_id)

            request.user = user
            return func(self, request)

        except KeyError:
            return JsonResponse({'message': 'AUTHORIZATION_KEY_ERROR'})
        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'})
        except DecodeError:
            debugger.exception('DecodeError')
            return JsonResponse({'message': 'DECODE_ERROR'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'})
    return wrapper
