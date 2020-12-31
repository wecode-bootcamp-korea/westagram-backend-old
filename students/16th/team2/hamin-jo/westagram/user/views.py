import json

from django.views import View
from django.http import JsonResponse

from user.models import User

class UserView(View):
    def sign_in(self, request):
