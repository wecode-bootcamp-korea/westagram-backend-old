import bcrypt
import json
import jwt

from decorator    import login_check
from django.http  import JsonResponse
from django.views import View

from my_settings  import SECRET
from .models      import User, Follow

# 회원가입
class SignUpView(View):
    def post(self, request): 
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({'message': '이미 사용중인 email'}, status=400)

            if '@' and '.' not in email:
                return JsonResponse({'message': '잘못된 email 형식'}, status=400)
            if len(password) < 8:
                return JsonResponse({'message': '비밀번호 길이는 8글자 이상'}, status=400)

            User(
                #name     = name,
                password = hashed_password,
                #phone    = phone,
                email    = email).save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


# 로그인
class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            password  = data['password']

            if 'email' in data:
                email = data["email"]
                user =  User.objects.get(email=data["email"])
                password_check = user.password
                if bcrypt.checkpw(password.encode('utf-8'), password_check.encode('utf-8')):
                    token = jwt.encode({'id': user.id}, SECRET, algorithm='HS256')
                    return JsonResponse({'token':token}, status=200)
                else:
                     return JsonResponse({'message':'비밀반호 오류'}, status=401)
            else:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'존재하지 않는 계정입니다.'}, status=400)

# follow하기
class FollowView(View):
    @login_check
    def post(self, request, user_id):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(id=user_id)
            follower = request.user # 로그인 하면서 받는 유저

            if follower.id == user_id:
                return JsonResponse({'message':'자기 자신은 follow할 수 없습니다.'}, status=400)
            
            if Follow.objects.filter(user=user_id, follower=follower): # unfollow
                Follow.objects.filter(user=user_id, follower=follower).delete()
            else:
                Follow.objects.create(user=user, follower=follower)
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except User.DoesNotExist :
            return JsonResponse({'message':'해당하는 유저가 없습니다.'}, status=400)

