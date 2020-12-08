import json 

from django.views import View
from django.http import JsonResponse

from .models import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if "@" not in data['email'] or "." not in data['email']:
                return JsonResponse({'MESSAGE':'EMAIL_ERROR!'}, status=400)

            if len(data['password']) < 8:
                 return JsonResponse({'MESSAGE':'PASSWORD_IS_SHORT!'}, status=400)

            if User.objects.filter(email=data['email']):
                return JsonResponse({'MESSAGE':'EMAIL_ALEADY_IN_USE'}, status=400)

            User.objects.create(
                email = data['email'],
                password = data['password'],           
                )
            return JsonResponse({'MESSAGE':'SUCCESS!'}, status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEYERROR!"}, status=400)
       
            