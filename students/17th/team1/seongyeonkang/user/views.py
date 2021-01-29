import json

from django.http        import JsonResponse
from django.views       import View
from django.db.utils    import DataError

from user.models    import User

class UserView(View):
    def post(self, request):
        data  = json.loads(request.body)
        
        if not data['email'] or not data['password']:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        if '@' not in data['email'] or '.' not in data['email'] or data['email'] == '@.':
            return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status=400)

        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXIST'}, status=400)

        if len(data['password']) < 8:
            return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=400)

        try:
            email = User.objects.create(
                email=data['email'],
                password=data['password']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except DataError:
            return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
        
