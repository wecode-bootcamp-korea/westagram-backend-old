from json

from django.views import View

from .models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        email    = User.objects.get(name=data['email'])
        password = User.objects.get(name=data['password'])
        user     = User.objects.create(
            email    = data['email']
            password = data['password']
        )
        if '@' and '.' in email and len(password) >= 8:
            return JsonResponse({"message": "SUCCESS"}, status_code=200)
        else:
            return JsonResponse({"message": "KEY_ERROR"}, status_code=200)
        
        