import json
import jwt
from django.http import JsonResponse
from django.db.models import Q
from user.models import (
                        Users,
                    )

def getUserID(user_input):
    q = Users.objects.filter(
                    Q(name          = user_input)|
                    Q(phone_number  = user_input)|
                    Q(email         = user_input)
                    )

    if q.exists():
        return q[0].id
    else:
        return None

def checkAuthorization(token):
    import my_settings

    try:
        user_data   = jwt.decode(token, my_settings.SECRET['secret'], algorithm='HS256')
        user_id     = user_data['user_id']
    except jwt.InvalidSignatureError:
        return None

    if Users.objects.filter(id=user_id).exists():
        return user_id
    else:
        return None


def checkRequestBody(request):
    try:
        data    = json.loads(request.body)
        return None
    except Exception as ex:
        return JsonResponse({"message":"You've requested with wrong JSON format."}, status=400)

