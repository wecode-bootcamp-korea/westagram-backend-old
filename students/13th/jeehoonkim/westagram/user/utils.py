import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY

def authorize_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        
        try:
            token=request.headers.get('Authorization')
            payload=jwt.decode(token, SECRET_KEY, algorithm='HS256')
            request.user=payload['user_id']            

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)

    return wrapper
        

