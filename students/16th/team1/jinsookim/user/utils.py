import json
from .models import Users
from posting.models import Post_register
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
def login_decorator(func):
    a = 10
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = data['user']
        try:
            if Users.objects.filter(email = user).exists() == False:
                return JsonResponse({'message' : '알 수 없는 사용자입니다.'}, status=401)
        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=401)
        return func(self, request, *args, **kwargs)
    return wrapper