import json
import re
import bcrypt

from django.views   import View
from django.http    import JsonResponse

from .models            import User
from decorators.utils   import check_blank

class UserSignUpView(View):
    @check_blank
    def post(self, request):
        data     = json.loads(request.body)
        email    = data["email"]
        password = data["password"]
        try:
            regex = re.compile("[a-zA-Z0-9-_.]+@[a-z]+\.[a-z]+")
            clean_email =regex.match(email).string
        except AttributeError:
            return JsonResponse({"message":"NOT_EMAIL_FORMAT"}, status = 400)
        user = User.objects.filter(email = clean_email)
        
        if user.exists():
            return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 400)
        if len(password) < 8:
            return JsonResponse({"message":"PASSWORD_IS_AT_LEAST_8"}, status = 400)

        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        User.objects.create(email = clean_email, password = hash_password.decode())
        return JsonResponse({"message":"SUCCESS"}, status = 200)

class UserSignInView(View):
    @check_blank
    def post(self, request):
        data        = json.loads(request.body)
        email       = data["email"]
        password    = data["password"]

        try:
            user = User.objects.get(email = email)
            password_check = bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))
            if password_check:
                return JsonResponse({"message":"SUCCESS"}, status = 200)    
            return JsonResponse({"message":"PASSWORD_IS_WRONG"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 401)
        
            