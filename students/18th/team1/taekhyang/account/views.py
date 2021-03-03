import json

from django.views     import View
from django.http      import JsonResponse


class SignUpView(View):
    def post(self, request):
        data = request.body
        