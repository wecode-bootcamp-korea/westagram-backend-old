import json
import bcrypt

from django.http    import JsonResponse
from django.views   import View
from user.models    import User

# Create your views here.

class SignupView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            if ('@' not in data['email'] or 
                '.' not in data['email']):
                return JsonResponse(
                    {'MESSAGE': 'Invalid Email'},
                    status=403)
            elif len(data['password']) < 8:
                return JsonResponse(
                    {'MESSEAGE': 'The password length should be greater than 7.'},
                    status=400)
            elif (User.objects.filter(email = data['email']).exists() or 
                User.objects.filter(username = data['username']).exists()):
                return JsonResponse(
                    {'MESSAGE': 'The given information has been already taken.'},
                    status=403)
            else:
                User(
                    mobile      = data['mobile'],
                    email       = data['email'],
                    full_name   = data['full_name'],
                    username    = data['username'],
                    password    = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt() ) #디코드해서 저장^^..
                ).save()
                return JsonResponse(
                    {'MESSAGE':'REGISTER_SUCCESS'}
                    , status=201)

        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, 
                status=400)

class LoginView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            hashed_pw = bcrypt.hashpw( data['password'].encode('utf-8'), salt )
            if 'email' in data.keys():
                if User.objects.filter(email = data['email']).exists():
                    if bcrypt.checkpw( hashed_pw , User.objects.get(email = data['email']).password.encode('utf-8') ):
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            elif 'mobile' in data.keys():
                if User.objects.filter(mobile = data['mobile']).exists():
                    if bcrypt.checkpw( hashed_pw , User.objects.get(mobile = data['mobile']).password.enconde('utf-8')):
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            elif 'username' in data.keys():
                if User.objects.filter(username = data['username']).exists():
                    if bcrypt.checkpw( hashed_pw , User.objects.get(username = data['username']).password.encode('utf-8') ):
                        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
                    else:
                        return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
                else:
                    return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'},
                status=400)


#class FollowingView(View):
#    def post(self, request):
#        data = json.loads(request.body)

        # http POST localhost:8000/follow follower="" following="" 
       
#        user_following = User.objects.get(username = data['following'])
#        user_followed = User.objects.get(username = data['followed'])

#        user_following.is_following.add(data['followed'])
#        user_followed.is_followed.add(data['following'])

#        User.objects.get(username = data['following']).is_following.add(data['followed'])
#        User.objects.get(username = data['followed']).is_followed.add(data['following'])
    

#        return JsonResponse(
#            {'MESSAGE': 'FOLLOW'},
#            status=200)

class FollowingView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if User.objects.filter(id = data['follower'], follow = data['following']).exists():
            unfollow = User.objects.get(id = data['follower'])
            unfollow.follow.remove(data['following'])

            return JsonResponse(
                {'MESSAGE': 'UNFOLLOW'},
                status=200)

        else:
            follower = User.objects.get(id = data['follower'])
            follower.follow.add(data['following'])
        
            return JsonResponse(
                {'MESSAGE':'FOLLOW'},
                status=200)
