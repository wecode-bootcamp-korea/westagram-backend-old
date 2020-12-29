import json

from django.http import JsonResponse


def check_blank(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        value_list = data.values()
        if "" in value_list:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper