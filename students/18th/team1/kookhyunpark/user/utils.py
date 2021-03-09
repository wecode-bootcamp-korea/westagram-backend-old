import jwt
from datetime import datetime, timedelta

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM

def LoginCheck(user_id):
    exp = datetime.utcnow() + timedelta(hours = 1)
    access_token = jwt.encode(
        {
            "user_id" : user_id,
            "exp"     : exp
        }, SECRET_KEY, ALGORITHM)
    #print(access_token)
    #return JsonResponse({'Authorization':access_token}, status=200)
    return access_token