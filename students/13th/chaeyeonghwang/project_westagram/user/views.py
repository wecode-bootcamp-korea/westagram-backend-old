import json

from django.http import JsonResponse
from django.views import View
from user.models import User

# Create your views here.

class SignupView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            if ('@' not in data['email'] or 
                '.' not in data['email']):
                return JsonResponse(
                    {'MESSAGE': 'Invalid Email'},
                    status=403)
            elif len(data['password']) < 8:
                return JsonResponse(
                    {'MESSEAGE': 'The password length should be greater than 7.'},
                    status=400)
            elif (User.objects.filter(email = data['email']).exists() or 
                User.objects.filter(username = data['username']).exists()):
                return JsonResponse(
                    {'MESSAGE': 'The given information has been already taken.'},
                    status=403)
            else:
                User(
                    mobile      = data['mobile'],
                    email       = data['email'],
                    full_name   = data['full_name'],
                    username    = data['username'],
                    password    = data['password']
                ).save()
                return JsonResponse(
                    {'MESSAGE':'REGISTER_SUCCESS'}
                    , status=200)

        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, 
                status=400)

class LoginView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'email' in data.keys():
                if User.objects.filter(email = data['email']).exists():
                    if User.objects.get(email = data['email']).password == data['password']:
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            elif 'mobile' in data.keys():
                if User.objects.filter(mobile = data['mobile']).exists():
                    if User.objects.get(mobile = data['mobile']).password == data['password']:
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            elif 'username' in data.keys():
                if User.objects.filter(username = data['username']).exists():
                    if User.objects.get(username = data['username']).password == data['password']:
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
#            if (User.objects.get(mobile = data['mobile']).password    != data['password'] or 
#                User.objects.get(email = data['email']).password        != data['password'] or 
#                User.objects.get(username = data['username']).password  != data['password']):
#                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
#            elif (User.objects.filter(mobile = data['mobile']).exists() or 
#                User.objects.filter(email = data['email']).exists() or 
#                User.objects.filter(username = data['username']).exists()):
#                return JsonReponse({'MESSAGE':'SUCCESS'}, status=200)
#            else:
#                return JsonResponse(
#                    {'MESSAGE':'INVALID_USER'},
#                    status=401)
        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'},
                status=400)
