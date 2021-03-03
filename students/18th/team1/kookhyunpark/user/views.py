import json

from django.http  import JsonResponse, request
from django.views import View

from user.models import User

class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create(
            email         = data['email'],
            phone         = data['phone'],
            full_name     = data['full_name'],
            user_name     = data['user_name'],
            password      = data['password'],
            date_of_birth = data['date_of_birth'],
        )
        
        #user = User.objects.get

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
