import json
from django.http    import JsonResponse
from django.views   import View
from users.models   import User,Following

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)

        if data.get('email',None) == None or data.get('password',None) == None or data.get('name',None) == None:
            return JsonResponse({'message':'email or password or name is vacant'},status=401)

        if len(data['password']) < 5:
            return JsonResponse({'message':'Password must be at least 5 chracters.'},status=401)
        
        if '@' not in data['email']:
            return JsonResponse({'message':'Invalid email format'},status=401)
        
        User(
            name        = data['name'],
            email       = data['email'],
            password    = data['password']
        ).save()

        return JsonResponse({'message':'Register Success'},status=200)

class SignInView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email=data['email']).exists():
                login_user = User.objects.get(email=data['email'])

                if login_user.password == data['password']:
                    return JsonResponse({'message':'SUCCESS'},status=200)

                return JsonResponse({'message':'INVALID_PASSWORD'},status=401)

            return JsonResponse({'message':'INVALID_USER'},status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'},status=400)

class FollowUserView(View):
    def post(self,request):
        data = json.loads(request.body)

        if data.get('followed_user_id',None) == None or data.get('following_user_id',None) == None:
            return JsonResponse({'message':'followd user id or following user id is vacant.'},status=401)

        if User.objects.filter(id=data['followed_user_id']).exists() and User.objects.filter(id=data['following_user_id']).exists():
            Following(
                   followed_user_id     =   data['followed_user_id'],
                   following_user_id    =   data['following_user_id']
                   ).save()

            return JsonResponse({'message':'SUCCESS'},status=200)

        return JsonResponse({'message':'INVALID_User_id'},status=401)
