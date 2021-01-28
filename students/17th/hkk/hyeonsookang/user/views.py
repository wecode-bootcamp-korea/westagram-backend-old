import json

from django.http  import JsonResponse

from django.views import View

from user.models  import Id, Password

class SignupView(View):

    def post(self, request):
        try:
            data             = json.loads(request.body)
            passwordvalidity = len(data['password'])

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE': 'INVALID__EMAIL'}, status=401)

            if Id.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_SIGNUP'}, status=401)

            if passwordvalidity < 8:
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)

            email            = Id.objects.create(email=data['email'])
            password         = Password.objects.create(
                                password=data['password'],
                                ids=email
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

