import json

from django.http import JsonResponse
from django.views import View

from user.models import User

# Create your views here.


class Posting(View):
    def posting(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            password = data['password']
        except:
            pass
