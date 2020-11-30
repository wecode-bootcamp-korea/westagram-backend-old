import jwt
import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .my_settings import SECRET, ALGORITHM
from user.models import User


def login_decorator(original_function):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            # print(access_token)
            # request header에서 토큰을 가져옴
            payload = jwt.decode(
                access_token, SECRET["secret"], algorithms=ALGORITHM["algorithm"],
            )  # 토큰을 다시 디코드함

            # print(payload)

            user = User.objects.filter(
                Q(user_name=payload["account"])
                | Q(mobile_number=payload["account"])
                | Q(email=payload["account"])
            )
            # 디코딩한 값의 정보와 동일한 객체를 user변수에 할당

            request.user = (
                user.first()
            )  # 변수 user를 request의 user 객체로 저장. 이는 데코레이터의 인자로 받을 함수에서 사용할 수 있도록 하기 위해서. 토큰 정보를 확인하는 HTTP Request 에는 토큰을 제외하고 사용자 정보 안들어와서 이 user값을 저장해서 이후 활용한다.
            # 이는 데코레이터의 인자로 받을 함수에서 사용할 수 있도록 하기 위해서 이다. 토큰 정보를 확인하는 HTTP Request 에는 토큰을 제외하고는 사용자 정보가 들어오지 않기 때문에, 이 user 값을 저장해서 이후 활용한다.
            # user 라는 새로운 속성을 만든 것임(header, body 이런 속성처럼)

        except jwt.DecodeError:
            return JsonResponse({"message": "invalid token!!"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "invalid user"}, status=400)

        return original_function(self, request, *args, **kwargs)

    return wrapper

