import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from account.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token    = request.headers.get('Authorization')
            playload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            user     = User.objects.get(id=playload['user_id'])
            
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=400)

        return func(self, request, *args, **kwargs)
    
    return wrapper
