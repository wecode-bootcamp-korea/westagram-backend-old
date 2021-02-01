import json

from django.views import View
from django.http  import JsonResponse, HttpResponse
from . models     import User


class UserView(View):
    def post(self, request):
        data = jsons.load(request.body)
        if 'email' not in data.keys() or 'password' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        elif len(data['password']) < 8:
            return
        elif '@' not in data['email'] or '.' not in data['email']:
            return
        else:
            return JsonResponse({'message': 'SUCCESS'}, status=200)





