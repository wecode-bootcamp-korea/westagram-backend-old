import json, bcrypt, jwt

from django.views       import View
from django.http        import JsonResponse

from .models            import User, Follow
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message': "EXIST_EMAIL"}, status=400)
            if ('@' in data['email']) and (len(data['password']) >= 5):
                User(
                    email    = data['email'],
                    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                ).save()
                return JsonResponse({'message': 'PERMISSION_MEMBERS'}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_INPUT'}, status=400)
        except KeyError:
            return JsonResponse({"message":"INVLID_INPUT"}, status=400)

    def get(self, request):
        user_data = user.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):    
                    user  = User.objects.get(email = data['email'])
                    token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
                    return JsonResponse({'success': token}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
            else:
                return JsonResponse({'message': 'NOT_MEMBERS'}, status=401)
        except KeyError:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

class FollowView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            follow   = User.objects.filter(email = data['email1'])
            followee = User.objects.filter(email = data['email2'])
            if follow[0] and followee[0]:
                if Follow.objects.filter(follow_user = follow[0]).exists():
                    follow_user = Follow.objects.get(follow_user = follow[0].id)
                    if follow_user.followee_user == followee[0]:
                        follow_user.delete()
                        return JsonResponse({'message': 'UNFOLLOW'}, status=200)
                    else:
                        follow_user.followee_user = followee[0]
                        return JsonResponse({'message': 'FOLLOW'}, status=200)
                else:
                    Follow (
                        follow_user   = follow[0],
                        followee_user = followee[0]
                    ).save()
                    return JsonResponse({'message': 'FOLLOW'}, status=200)
            else:
                return JsonResponse({'message': 'NOT_MEMBER'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'INVALID_INPUT'}, status=400)
