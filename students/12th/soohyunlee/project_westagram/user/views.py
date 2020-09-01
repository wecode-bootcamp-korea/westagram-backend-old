import jason

from django.views import view
from django.http import JsonResponse
from jdango.models import User

class SignUp(view):
    user_name = data
    def get(self, request):
        if User.objects.filter():
            return jsonResponse({message}:{'Email does not match'})

