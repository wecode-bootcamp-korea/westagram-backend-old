import json

from django.views import View
from django.http import JsonResponse

class Signup(view):
    def get(self, request):
        return JsonREsponse({"message":"KEY_ERROR"}, status = 400)