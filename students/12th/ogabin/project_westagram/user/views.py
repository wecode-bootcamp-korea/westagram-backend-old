import json
from django.http  import JsonResponse
from django.views import View
from .models      import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        User(
            name         = data["name"],
            email        = data["email"],
            password     = data["password"],
            phone        = data["phone"],
        ).save()
        return JsonResponse({"message":"SUCCESS"}, status = 200)    

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'User':list(user_data)}, status = 200)