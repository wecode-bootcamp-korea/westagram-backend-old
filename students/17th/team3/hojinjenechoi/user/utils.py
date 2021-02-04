# import jwt
# import json
# import requests

# from django.http import HttpResponse
# ##
# from .models import User 

# def login_decorator(func):
#     def wrapper(self,request,*args, **kwargs):
#         payload = json.loads(request.body) ## body??
#         #token check?
#         user = User.objects.get(id=)
#         request.user = user

#         if User.DoesNotExist():
#            return JsonResponse({'message':'INVALID_USER'}, status:401)

#         return wrapper
#    

