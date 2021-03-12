import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User, Follow
from my_settings import SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EMAIL_ERROR"}, status=400)
            
            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({"message":"EMAIL_FAIL"}, status=400)
            if len(data['password']) < 8:
                return JsonResponse({"message":"PASSWORD_TOO_SHORT"}, status=400)

            byted_password = data['password'].encode('utf-8')
            hash_password = bcrypt.hashpw(byted_password, bcrypt.gensalt()).decode()
            password = hash_password
            user     = User.objects.create(
                email    = data['email'],
                password = password
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
   

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            try:
                user    = User.objects.get(email=data['email'])
                # user는 객체다
                user_id = user.id
                # 객체에 .~하면 바로 내용을 꺼낼 수 있다.
            except User.DoesNotExist:
                return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id' : user_id}, SECRET_KEY, algorithm="HS256")
                # 유저 id를 토큰 내용물을 넣는다. 이떄 이미 숫자가 나왔으므로 data로 할 필요 없음
                return JsonResponse({'token' : token, "message":"SUCCESS"}, status=200)
            
            return JsonResponse({"message":"INVALID_USER"}, status=401)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        
class TokenCheckView(View):
    def post(self,request):
        data = json.loads(request.body)
        
        user_token_info = jwt.decode(data['token'], SECRET_KEY, algorithms='HS256')
        
        if User.objects.filter(email=user_token_info['email']).exists():
            return JsonResponse({"message": "SUCCESS"}, status=200)
        return JsonResponse({"message":"INVALID_USER"}, status=401)
 
class FollowView(View):
    def post(self, request):
            data      = json.loads(request.body)
            following = User.objects.get(email=data['following'])
            follower = User.objects.get(email=data['follower'])
            if following == follower:
                return JsonResponse({"message":"SAME_PERSON!"})
                follow = Follow.objects.create(
                    following = following,
                    follower  = follower
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

def TokenCheck(func):
    def wrapper(self, request, *args, **kwargs):
    # 리퀘스트해서 토큰 까는 애
        # 토큰의 핵심은 공개가 되어도 된다 -> 그래서 예제가 user_id였던 것.
        try:
            token = request.headers.get('Authorization')
            if token:
                payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                # user_id 가져온 것을 user라는 변수에 담고
                
                request.user = user
                # 변수에 담은 것을 뒤에서 부를 request.user에 또 담아준다.
                return func(self, request, *args, **kwargs)
                # 얘는 return하면서 request를 posting에서 사용할 예정(.user 만 붙이면 이제 자동 완성)
            return JsonResponse({"message":"GIVE_ME_TOKEN"}, status=400)
        except jwt.InvalidTokenError:
            return JsonResponse({"message":"YOUR_TOKEN_ERROR"}, status=400)
        
        # 지금은 숫자만 확인 상황(id값만 받아서 확인한 상황) 
        # 추가 : 토큰을 다시 안 갖다준 상황(리퀘스트에 정보를 넣어준다.) ; 리퀘스트의 인스턴스를 만들어준다.(아이디값을 넣어준다.->이걸 꺼내 쓴다.)

    return wrapper