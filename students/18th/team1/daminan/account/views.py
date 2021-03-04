import json

from django.views import View
from django.http  import JsonResponse


from .models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)

        if '@' in data['email'] and '.' in data['email'] and len(data['password']) >= 8:
            user     = User.objects.create(
            email    = data['email'],
            password = data['password']
        )
            return JsonResponse({"message": "SUCCESS"}, status=200)
        else:
            return JsonResponse({"message": "KEY_ERROR"}, status=200)
        
        

        
        