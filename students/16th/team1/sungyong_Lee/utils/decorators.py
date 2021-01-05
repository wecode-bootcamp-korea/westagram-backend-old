import functools, json, jwt

from django.http    import JsonResponse
from my_settings    import SECRET_KEY
from account.models import User


class LoginCahsed(object):
    def __init__(self, func):
        self.func  = func
        self.cache = {}
        functools.update_wrapper(self, func)

    def __call__(self, request, *args, **kwargs):
        try:
            token   = request.headers['AUTHORIZATION']
            payload = jwt.decode(token, SECRET_KEY, algorithms = "HS256")
            user    = User.objects.get(pk = payload.get('user_id'))
            request.user = user
            
            return self.func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse(
                {
                    'message': 'LOGIN_REQUIRED'
                }, status=401)

# def login_cahsed(func):
#     @functools.wraps(func)
#     def wrapper(*args):
#         token = request.headers['AUTHORIZATION']
#         jwt.decode(token, SECRET_KEY, algorithms = "HS256")
#         return func(*args)
#     return wrapper

        
            
                
                
                


