import json

from django.http        import JsonResponse
from django.views       import View
from user.models        import User

# sign up
class Signup(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            if data.get('user_name') is not None:
                if data.get('password') is not None:
                    if User.objects.filter(user_name=data['user_name']) > 0:
                        return JsonResponse({'message':'KEY_ERROR'}, status=400)
                    if len(data.get('password')) < 5:
                        return JsonResponse({'message':'KEY_ERROR'}, status=400)
                    User.objects.create(
                        user_name   = data['user_name'],
                        password    = data['password']
                    )
                    return JsonResponse({'message':'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message':'KEY_ERROR'}, status=400)
            else:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

# sign in
class Signin(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_count = User.objects.filter(user_name=data['user_name']).count()
            signin_check = User.objects.get(user_name=data['user_name'])
            print(user_count)
            print(signin_check)
            print(signin_check.user_name)
            print(data['user_name'])
            print(signin_check)
            if user_count == 1:
                if signin_check.user_name == data['user_name'] and signin_check.password == data['password']:
                    return JsonResponse({'message':'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)    
        except:
            return JsonResponse({'message':'INVALID_USER'}, status=401)


# logout

