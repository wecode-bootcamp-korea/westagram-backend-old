import jwt

from westa.my_settings import SECRET_KEY, JWT_algorithm
from user.models       import User

def login_decorator(func):
    def wrapper(self,request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        payload = jwt.decode(access_token,SECRET_KEY['secret'], algorithm=JWT_algorithm)
        user = User.objects.get(id = payload['id'])
        request.user = user.id

        return func(self, request, *args, **kwargs)

    return wrapper
