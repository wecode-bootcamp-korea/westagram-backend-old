from collections import namedtuple
import json, re
import bcrypt
import jwt

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import User, Follow
from my_settings        import SECRET_KEY,AL
from posting.utils      import login_decorator

class UserView(View):
    def post(self, request):
        email_valid     = "[0-9a-zA-Z_-]+[@]{1}[0-9a-zA-Z_-]+[.]{1}[a-zA-Z]+"
        password_valid  = ".{8,}"
        name_valid      = "^(?=.*[a-z])[0-9a-zA-Z]+"
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hash_password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            name            = data['name']
            phone_number    = data['phone_number']
            
            if User.objects.filter(Q(email=email)|Q(name=name)|Q(phone_number=phone_number)).exists():
                return JsonResponse({'message' : 'EXISTING_USER'}, status=400)
            if not re.search(email_valid, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)
            if ' 'in (email and password):
                return JsonResponse({'message' : 'MEANINLESS_SPACE'}, status=400)
            if not re.search(password_valid, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=400)
            if not re.search(name_valid, name):
                return JsonResponse({'message' : 'INVALID_NAME'}, status=400)
            User.objects.create(
                    email=email,
                    password=hash_password.decode('utf-8'),
                    name=name,
                    phone_number=phone_number
                    )
            return JsonResponse({'meassage' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            password        = data.get('password', None)
            login_id        = data.get('login_id', None)
            
            if not (login_id and password):
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
            if not User.objects.filter(Q(email=login_id) | Q(name=login_id) | Q(phone_number=login_id)).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            user = User.objects.get(Q(email=login_id)|Q(name=login_id)|Q(phone_number=login_id))
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            
            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm=AL)
        #    check_token = jwt.decode(access_token, SECRET_KEY, algorithms = AL) #user_id='id' 의 형태로 나온다. = 딕셔너리!!

            return JsonResponse({'message' : '로그인 성공', "token" : access_token}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class FollowView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = User.objects.get(id=request.user.id)
            following   = User.objects.get(name=data['following'])
            
            if Follow.objects.filter(user_id=user.id, following_id=following.id).exists():
                return JsonResponse({'message' : 'ALREADY_DONE'}, status=400)

            Follow.objects.create(user_id = user.id, following_id = following.id)

            return JsonResponse({'result' : '\''+user.name+'\''+' start following'+'\''+following.name+'\''}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    def get(self, request):
        try:
            if not request.body:
                follows = Follow.objects.all()
            # 특정 user의 name을 입력하면 그 user의 follower만 보여준다
            else:
                data    = json.loads(request.body)
                user    = User.objects.get(name = data['user'])
                follows = Follow.objects.filter(user_id = user.id)
            
            follow_list = []
            for follow in follows:
                follow_info = {
                        'user' : follow.user.name,
                        'follower' : follow.following.name,
                        }
                follow_list.append(follow_info)

            if not follow_list :
                return JsonResponse({'result' : 'NONE'}, status=200)
            return JsonResponse({'result' : follow_list}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class FollowDetailView(View):
    @login_decorator
    def get(self, request, user_id):
        user    = request.user
        follows = Follow.objects.filter(user_id = user.id)

        follow_list = []
        for follow in follows:
            follow_info = {
                    'following' : follow.following_id
                    }
            follow_list.append(follow_info)
        return JsonResponse({'result' : follow_list}, status=200)
    
    @login_decorator
    def delete(self, requeste, user_id):
        user        = requeste.user
        following   = User.objects.get(id=user_id)

        if not Follow.objects.filter(user_id=user.id, following_id=following.id).exists():
            return JsonResponse({'message' : 'NOT_FOLLOWING'}, status=400)
        follow  = Follow.objects.get(user_id=user.id, following_id=following.id)
        follow.delete()

        return JsonResponse({'result' : 'BYE BYE'}, status=200)
