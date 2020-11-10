import jwt
import json

from django.conf import settings
from django.http import JsonResponse

from .models     import User

def key_error_decorator(func):
    '''
        request가 있는 값에서는 계속해서 원하는 인자가 있는지 확인하는
        로직이 반복적으로 쓰인다고 느낍니다.
        이것을 내가 정의해놓은 키와 request 헤더를 인자로 받아 데코레이터로
        만들어 쓰는게 좋은걸까요?
    '''
    pass

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):

        data = json.loads(request.body)
        if 'authorization' not in data.keys():
            return JsonResponse({'message': 'DO_NOT_EXIST_TOKEN'}, status=400)

        encode_token = data['authorization'].encode('utf-8')

        try:

            decode_data = jwt.decode(encode_token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=decode_data['id'])

            request.user = user

        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'DO_NOT_EXIST_USER'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper
