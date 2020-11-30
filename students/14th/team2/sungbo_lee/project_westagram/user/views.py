import json
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db        import IntegrityError
from django.db.models import Q

from user.models                import User
from project_westagram.settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email        = data["email"]
            password     = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            phone_number = data["phone_number"]
            name         = data["name"]

            if '@' not in email:
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            if '.' not in email:
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            if len(password) < 8:
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            if User.objects.filter(email=email):
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            if User.objects.filter(phone_number=phone_number):
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            if User.objects.filter(name=name):
                return JsonResponse({'message': 'INVALID_KEY'}, status=400)

            user = User(
            email        = email,
            password     = password,
            phone_number = phone_number,
            name         = name,
            )

            user.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        except IntegrityError:
            return JsonResponse(status=400)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email        = data['email']
            password     = data['password']

            if not User.objects.get(email=email):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

                payload = {"id": user.id}

                token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
                return JsonResponse({"token": token}, status=200)
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)
