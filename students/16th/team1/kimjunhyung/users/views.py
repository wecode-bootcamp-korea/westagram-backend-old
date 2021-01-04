import json
import re
import bcrypt
import jwt

from django.views   import View
from django.http    import JsonResponse

from .models            import User, Follow
from decorators.utils   import check_blank, login_required, get_user
from my_settings        import SECRET_KEY

class UserSignUpView(View):
    @check_blank
    def post(self, request):
        data     = json.loads(request.body)
        email    = data["email"]
        password = data["password"]
        try:
            regex        = re.compile("[a-zA-Z0-9-_.]+@[a-z]+\.[a-z]+")
            clean_email  = regex.match(email).string
        except AttributeError:
            return JsonResponse({"message":"NOT_EMAIL_FORMAT"}, status = 400)
        user = User.objects.filter(email = clean_email)
        
        if user.exists():
            return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 400)
        if len(password) < 8:
            return JsonResponse({"message":"PASSWORD_IS_AT_LEAST_8"}, status = 400)

        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        User.objects.create(email = clean_email, password = hash_password)
        return JsonResponse({"message":"SUCCESS"}, status = 200)

class UserSignInView(View):
    @check_blank
    def post(self, request):
        data        = json.loads(request.body)
        email       = data["email"]
        password    = data["password"]
        
        try:
            user = User.objects.get(email = email)
            password_check = bcrypt.checkpw(password.encode("utf-8"), user.password)
            if password_check:
                encoded_jwt = jwt.encode(
                    {"id":user.id}, key = SECRET_KEY, algorithm = "HS256"
                )
                return JsonResponse({"message":"SUCCESS", "token":encoded_jwt}, status = 200)    
            return JsonResponse({"message":"PASSWORD_IS_WRONG"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 401)

class FollowUser(View):
    @login_required
    def post(self, request):
        data            = json.loads(request.body)
        token           = json.loads(request.headers.get("Token"))
        follower        = get_user(token)
        following_id    = data["user_id"]
        
        try:
            following   = User.objects.get(id = following_id)
            follow      = Follow.objects.filter(follow_user = follower, following_user = following).select_related("user")
            if follower == following:
                return JsonResponse({"message":"CAN_NOT_SELF_FOLLOW"}, status = 403)
            if follow.exists():
                follow.delete()
                return JsonResponse({"message":"UNFOLLOW"}, status = 200)
            follow.create(follow_user = follower, following_user =following)
            return JsonResponse({"message":"FOLLOW"}, status = 200)
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 401)
        
            
