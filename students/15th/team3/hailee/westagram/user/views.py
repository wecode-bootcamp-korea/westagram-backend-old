import json
import re

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
                    if User.objects.filter(user_name=data['user_name']).count() > 0:
                        return JsonResponse({'message':'DUPLICATED_USERNAME'}, status=400)
                    print(data.get('password'))
                    print(data['password'])
                    if re.search('[0-9]+', data['password']) is None:
                        print('비밀번호 re test')
                        return JsonResponse({'message':'TOO_SHORT_PW'}, status=400)
                    # if len(data.get('password')) < 8:
                    #     return JsonResponse({'message':'KEY_ERROR'}, status=400)
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
            if user_count == 1:
                if signin_check.user_name == data['user_name'] and signin_check.password == data['password']:
                    return JsonResponse({'message':'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)    
        except:
            return JsonResponse({'message':'INVALID_USER'}, status=401)


# logout

