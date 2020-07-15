import json
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse

from .models            import User
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': "EXIST_EMAIL"}, status=400)
            if ('@' in data['email']) and (len(data['password']) >= 5):
                User(
                    name = data['name'],
                    email = data['email'],
                    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                ).save()
                return JsonResponse({'message': 'PERMISSION_MEMBERS'}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_INPUT'}, status=400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

    def get(self, request):
        user_data = user.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(name=data['name']).exists:
                user = User.objects.get(name = data['name'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):    
                    user = User.objects.get(name = data['name'])
                    token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
                    return JsonResponse({'success': token}, status=200)
                else:
                    return JsonResponse({'messgae': 'INALID_PASSWORD'}, status=403)
            else:
                return JsonResponse({'message': 'NOT_MEMBERS'}, status=401)
        except KeyError:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
