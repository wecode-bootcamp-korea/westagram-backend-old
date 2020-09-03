import json
from django.views import View
from django.http  import JsonResponse
from user.models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
    

        try:
            if data['name'] and data['email'] and data['password']:

                if '@' not in data['email'] or '.' not in data['email']:
                    return JsonResponse({'message':'Invalid format'}, status = 400)

                if len(data['password']) < 10:
                    return JsonResponse({'message': 'Password must be at least 10 digits.'},
                        status = 400
                    )
            
            
                if Users.objects.filter(email=data['email']).exists():
                    return JsonResponse({'Already Exists'}, status=400)

                if Users.objects.filter(email=data['name']).exists():
                    return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
        
            Users.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password']
            ).save()

            return JsonResponse(
                {'message': 'SUCCESS'},
                status = 200
                )

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)



           
