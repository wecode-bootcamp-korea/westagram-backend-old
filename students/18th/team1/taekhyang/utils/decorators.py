import jwt
import sys, os
import json
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from project_westagram.settings import SECRET_KEY
from utils.debugger import debugger


def auth_check(func):
    def wrapper(self, request):
        data = request.headers
        try:
            encoded_auth_token = data['Authorization']
            decoded_auth_token = jwt.decode(encoded_auth_token, SECRET_KEY, algorithms='HS256')
            return func(self, request, decoded_auth_token)

        except KeyError:
            return JsonResponse({'message': 'AUTHORIZATION_KEY_ERROR'})
        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'})
        except DecodeError:
            debugger.exception('DecodeError')
            return JsonResponse({'message': 'DECODE_ERROR'})
    return wrapper
