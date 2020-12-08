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



            try:
                 if (data['name'] is not None) or (data['tel'] is not None) or (data['email'] is not None):
                    if data['password'] is not None:

                        if len(data['password']) < 8:
                            return JsonResponse({"message": "your password is dangerous."}, status= 401)

                        if ('@' not in data['email']) or ('.' not in data['email']):
                            return JsonResponse({'message':'its not email format'},status=401)

                        if SignUp.objects.filter(name = data['name']).exists() and SignUp.objects.filter(email = data['email']).exists() and SignUp.objects.filter(tel = data['tel']).exists():
                            return JsonResponse({'message':'your information is already registered.'},status=400)



                        SignUp(
                            tel=data['tel'],
                            email=data['email'],
                            name=data['name'],
                            password=data['password']
                        ).save()
                        return JsonResponse({"message": "SUCCESS"}, status=200)

            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)



class SignIn(View):
    def post(self,request):
        data = json.loads(request.body)
        data['email'] = data.get('email')
        data['tel'] = data.get('tel')
        data['name'] = data.get('name')

        try:
            if data['name'] is not None:
                if SignUp.objects.filter(name=data['email'], password=data['name']).exists():
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            if data['email'] is not None:
                if SignUp.objects.filter(email=data['email'], password=data['password']).exists():
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            if data['tel'] is not None:
                if SignUp.objects.filter(tel=data['email'], password=data['password']).exists():
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except:
             return JsonResponse ({'message': 'KEY_ERROR'}, status=400)

