import json
from django.http import JsonResponse
from user.models import User

# 로그인 체크
def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if not User.objects.filter(name=data['user']):
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper



# 들어오는 키값이 비어있을 경우 체크
