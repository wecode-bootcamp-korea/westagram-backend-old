import jwt
import json
import requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from project_westagram.settings import SECRET, ALGORITHM
from user.models import User


def login_decorator(original_function):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            print(access_token)
            payload = jwt.decode(
                access_token, SECRET["secret"], algorithms=ALGORITHM["algorithm"],
            )
            user = User.objects.filter(
                Q(user_name=payload["account"])
                | Q(mobile_number=payload["account"])
                | Q(email=payload["account"])
            )

            request.user = user.first()

        except jwt.DecodeError:
            return JsonResponse({"message": "invalid token!!"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "invalid user"}, status=400)

        return original_function(self, request, *args, **kwargs)

    return wrapper

