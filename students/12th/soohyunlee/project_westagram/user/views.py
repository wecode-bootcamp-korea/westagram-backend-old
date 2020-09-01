import json

from django.views import View
from django.http import JsonResponse
from .models import User

class MainView(View):
    def post(self, request):
        data = json.loads(request.body)
        Users(
            name = data['name'],
            email = data['email'],
            password = data['passowrd']
        ).save()

        if User.obects.filter(name = data['name']).exist():
            return JsonPesponse({'message':'Already_in_use'})
        if not '@' in 'email' and not '.' in 'email':
            return jsonResponse({'message':'Email_Form_Error'})
        if len(password) < 8:
            return jsonResponse({'message':'Password_Form_Error'})
        else:
            return jsonResponse({'message':'SUCCESS'}, statuse=200)
