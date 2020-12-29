import json

from django.http import JsonResponse

from users.models import User


def check_blank(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        value_list = data.values()
        if "" in value_list:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data['email']
        user = User.objects.filter(email = email)
        if not user.exists():
            return JsonResponse({"message":"LOGIN_REQUIRED"}, status = 401)
        return func(self, request, *args, **kwargs)
    return wrapper