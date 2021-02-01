import json
from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models      import UserPassword, Userinfo


class UserloginView(View):
    #def POST(self, request):
    pass   
