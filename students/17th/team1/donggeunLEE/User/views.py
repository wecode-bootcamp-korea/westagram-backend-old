import json
import bcrypt
import jwt

from django.http              import HttpResponse, JsonResponse
from django.views             import View
from django.db.models         import Q
from django.core.validators   import validate_email, ValidationError

from .models                  import Userinfo, Follow
import my_settings
from .utilities               import login_decorator

# 회원가입
MINIMUM_PASSWORD_LENGTH = 8                    # 변수명만 봐도 이게 먼지 알수있도록 줄이지 말고 적어준다. , 나중에 비교하는데 숫자가 많이 들어가게 될 경우도 있기때문에 넣어준다. 보이면 안되는 상수는 my_settings.에 넣어서 git에 올리지 않는다.
class UserSignUpView(View):
    #MINIMUM_PASSWORD_LENGTH = 8
    def post(self, request):
        data = json.loads(request.body)
                
        try:
            password_validity = data['password']

            if Userinfo.objects.filter(name = data['name']).exists():
                return JsonResponse({"MESSAGE" : "USER_ALREADY_EXIST"}, status = 400)
        
            if Userinfo.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({"MESSAGE": "INVALID_PHONE_NUMBER"}, status= 400)
        
            if Userinfo.objects.filter(email = data['email']).exists():
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)
        
            if '@' and '.' not in data['email']:
                return JsonResponse({"MESSAGE" : "Inavailed_KeyError"}, status= 400)
        
            if len(password_validity) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"MESSAGE" : "SHORT_PASSWORD"}, status= 400)

            Userinfo.objects.create(
                    name         = data['name'],
                    phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)
            
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

# 애초에 추가값을 넣어준 것이다. request.user = user 받은 request에 decorater를 하기 위 해서 만든 것이기 때문에 request에 user 값을 넣어 준것이다. 가변객체인 request에 추가적으로 정보를 달아서 넣으면 된다. 아하!!!!!!!!!!!!!!! header, startline, body에 추가적으로 user의 정보를 담아서 headet, startline, body, user가 되는 것이다!!!!!!!!!!!!!

# utilis.py에 넣어서 만들어 주고 import해서 해주면 된다, deorator나 공통적으로 사용할 수 있는 것을 넣는다. 전데 모든 프로젝트에 쓰인다면 cores나 이런것을 만들어서 import해서 사용해주는 방식으로 쓰면 된다.

# 정규식.............. input에 대한 validation은 귀찮아 하면 안된다. if 중첩적인 사항은 피하는 것이 좋다.
# 효율적인 code flow를 생각 하는게 중요 효율 효율 효율, else를 한개 줄이는게 중요!!!!! 생략할수 있는 else르 줄여서
# inden를  들여쓰지않게 하는 것이 좋다. 
# MESSAGE는 친절하지 않다면 굿이 JsonResponse를 써줄 필요가 없다. 써줄려면 메세지는 단순하고 !!! 알아들을 수 있도록
# 단순히 응답코드로써 보내자 시크하게


class UserlonginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)   
            name         = data.get('name', None)
            phone_number = data.get('phone_number', None)
            email        = data.get('email', None)
     
            if Userinfo.objects.filter(name = name).exists():
                user = Userinfo.objects.get(name = name)
                # db에 암호화한 비밀번호랑 받은 비밀번호를 비교해서 맞으면 토큰을 주고 아니면 오류메세지 리턴
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id' : user.id}, 'secret' , algorithm ='HS256').decode('utf-8')   
                    return JsonResponse({"TOKEN" : access_token},status=200)
                    #return JsonResponse({"TOKEN" : access_token, "MESSAGE":"SUCCESS"}, status = 200)
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status = 401)
            
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"MESSAGE": "INVALID_KEYS"}, status = 400)


class FollowView(View):
    # follower 팔로우를 할 사람, followee 팔로우를 걸 사람
    @login_decorator
    def post(self, request):
        try:
            data           = json.loads(request.body)
            follower_id    = request.user
            followee_id    = data['followee_id']


            if Follow.objects.filter(follower_id = follower_id, followee_id = followee_id).exists():
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)
        
            Follow.objects.create(
                    follower = follower_id,
                    followee = followee_id
                    )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE" : 'INVALID_KEY'}, status=400)

    
    @login_decorator
    def delete(self, request):
        data         = json.loads(request.body)
        follower     = request.user
        follower_id  = follower.id
        followee_id = data['followeee_id']

        if Follow.objects.filter(follower_id = follower_id, followee_id = followee_id).exists():
            Follow.objects.get(follower_id=follower_id, followee_id=followee_id).delete()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)


        










