import json
import os
import sys
import jwt
import bcrypt

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from user.models import User

def LoginAuthorization(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            token            = request.headers.get( 'Authorization' )
            token_payload    = jwt.decode( token, SECRET_KEY, algorithm = ALGORITHM )
            token_user_id    = token_payload['user_id']
            token_username   = token_payload['username']
            request.user_id  = token_user_id
            request.username = token_username
            return function(self, request, *args, **kwargs)

        except Exception as e:
            return JsonResponse({'ERROR':'SIGNUP_FIRST'})

    return wrapper






