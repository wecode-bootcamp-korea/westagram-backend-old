from django.shortcuts import render
import re
import json
from django.http     import JsonResponse
from .models   import SignUp
from django.views    import View

class SignUpView(View):


        def post(self, request):
            data = json.loads(request.body)

            data['email'] = data.get('email')
            data['tel'] = data.get('tel')
            data['name'] = data.get('name')

            SignUp(
               tel=data['tel'],
               email=data['email'],
               name=data['name'],
               password=data['password']
            ).save()
            return JsonResponse({"message": "SUCCESS"}, status=200)
            # return JsonResponse({data['email'],data['tel']})

            # try:
            #      if (data['user_name'] is not None) or (data['phone_number'] is not None) or (data['email'] is not None):
            #         if data['password'] is not None:
            #
            #             if len(data['password']) < 8:
            #                 return JsonResponse({"message": "your password is dangerous."}, status= 401)
            #
            #             if '@' not in data['email']:
            #                 return JsonResponse({'message':'its not email format'},status=401)
            #
            #             if User.objects.filter(email = data['email']).exists() or User.objects.filter(user_name = data['user_name']).exists() or User.objects.filter(phone_number = data['phone_number']):
            #                 return JsonResponse({'message':'your information is already registered.'},status=400)
            #
            #
            #      User.objects.create(
            #         user_name    = data['user_name'],
            #         phone_number = data['phone_number'],
            #         email        = data['email'],
            #         password     = data['password']
            #      )
            #      return JsonResponse({"message": "SUCCESS"}, status=200)
            #
            # except KeyError:
            #     return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            #data = json.loads(request.body)
            #User.objects.create(user_name = data['user_name'],password = data['password'])

            #return JsonResponse({"message" :"SUCCESS"}, status=201)