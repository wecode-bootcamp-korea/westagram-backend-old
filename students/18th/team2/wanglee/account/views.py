import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


from .models      import User


class UserSignup(View):
    def post(self, request):
        data     = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password']
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        username = data['username']
        phone_num    = data['phone_num']
        temps = User.objects.filter(username=username) | User.objects.filter(email=email) | User.objects.filter(phone_num=phone_num)

        if '@' not in email or '.' not in email:
            return JsonResponse({"message":"email must contain the '@' symbol and the period'.'"}, status=400)
        
        elif len(password) < 8:
            return JsonResponse({"message":"password must be at least 8 characters"}, status=400)
        
        for temp in temps:
            if username == temp.username:
                return JsonResponse({"message":"That username is taken. Try another"}, status=400)
        
            elif email == temp.email:
                return JsonResponse({"message":"That email is taken. Try another"}, status=400)
        
            elif phone_num == temp.phone_num:
                return JsonResponse({"message":"That phone is taken. Try another"}, status=400)

        User.objects.create(username=username, email=email, password=password, phone_num=phone_num)
        return JsonResponse({'result': 'SUCCESS'}, status=200)
            
        
class UserSignin(View):
    def post(self, request):
        users    = User.objects.all()
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        username = data['username']
        phone_num    = data['phone_num']
        temps = User.objects.filter(username=username) | User.objects.filter(email=email) | User.objects.filter(phone_num=phone_num) | User.objects.filter(password=password)

        if password == '':
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        elif email == '' and username == '' and phone_num == '':
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
            
        else:
            for temp in temps:
                if username == temp.username or email == temp.email or phone_num == temp.phone_num:
                    if password == temp.password:
                        return JsonResponse({'result': 'SUCCESS'}, status=200)
            return JsonResponse({"message":"INVALID_USER"}, status=401)