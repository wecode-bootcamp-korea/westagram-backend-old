import jwt
import json

from django.http            import JsonResponse
from westagram.settings     import SECRET
from westagram.my_settings  import ALGORITHM, SECRET

from user.models            import User
from posting.models         import Post

class LoginConfirm:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                payload = jwt.decode(token, SECRET, ALGORITHM)
                request.user = User.objects.get(id = payload['id'])
                return self.func(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE':'로그인 하세요'}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': '존재하지 않는 유저입니다'}, status=400)
            