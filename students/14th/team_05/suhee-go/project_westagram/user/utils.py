import jwt
import my_settings

from django.http import JsonResponse
from .models import User

secret = my_settings.SECRET
algorithm = my_settings.ALGORITHM

def login_required(func) :
    @wraps(func)
    def wrapper(self, request, *arg, **kwargs) :
        access_token = request.headers.get('Authorization', None)

        if access_token is not None :
            try :
                payload = jwt.encode(access_token, secret, algorithm)
            except jwt.InvalidTokenError :
                payload = None

            if payload is None :
                return JsonResponse({"message" : "TOKEN_DNEY"}, status = 400)

            user_id = payload['user_id']
            get_user = get_user_info(user_id)

            if user_id else None :
                pass
            else :
                return JsonResponse({"message" : "USER_ID_NONE"}, status = 401)

            return wrapper(*arg, **kwargs)
        return check_token
