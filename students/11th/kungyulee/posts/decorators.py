import json

from django.http import JsonResponse

from accounts.models import User

def is_admin(func):
    def wrapper_func(request, *args, **kwargs):
        #if request.user.is_admin == True:
        data = json.loads(request.body)
        user = User.objects.get(phone_number = data['phone_number'])
        if user.is_admin == True:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({'message' : 'not admin'}, status = 400)
    return wrapper_func
