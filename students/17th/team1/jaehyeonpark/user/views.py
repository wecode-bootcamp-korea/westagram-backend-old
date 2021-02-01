import json

from django.http  import JsonResponse
from django.views import View
from django.db.utils import DataError, IntegrityError

from user.models  import User

PASSWORD_MINIMUN_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

        try:
            email    = str(data['email'])
            password = str(data['password'])
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if "" in (email, password):
            return JsonResponse({'message':'NO_VALUE_ERROR'}, status=400)
        
        if '@' and '.' not in email:
            return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)

        if len(password) < PASSWORD_MINIMUN_LENGTH:
            return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)

        try:
            user     = User.objects.create(email=email, password=password)
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'message':'INTEGRITY_ERROR'}, status=400)
        
        return JsonResponse({'message':'SUCCESS'}, status=200)