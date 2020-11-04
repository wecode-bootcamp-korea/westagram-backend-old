import json
from django.views import View
from django.http import JsonResponse
from .models import Users

class UsersView(View):
    def get(self, request):
        return JsonResponse({"users_view": "hello"}, status=200)