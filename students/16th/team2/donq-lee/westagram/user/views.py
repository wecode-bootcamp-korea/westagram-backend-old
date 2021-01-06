import json
import bcrypt
import jwt
from django.views import View
from django.http  import JsonResponse
from user.models  import User
from my_settings  import SECRET_KEY

class UserSignUpView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        
        if not email or password:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'message':'EXIST_EMAIL'}, status = 400)
        if len(password) < 8:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
        if '@' not in email or '.' not in email:
            return JsonResponse({'message':'INVALID_EMAIL'}, status = 400)
        encoded_pw = password.encode('utf-8')
        hashed_pw  = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
        encrypt_pw = hashed_pw.decode('utf-8')
        User.objects.create(
            email    = email,
            password = encrypt_pw
            )
        return JsonResponse({'message':'SUCCESS'}, status = 200)

class UserSignInView(View):
    def post(self, request):
        data      = json.loads(request.body)
        email     = data.get('email')
        password  = data.get('password')

        if User.objects.filter(email = email).exists():
            signin_user = User.objects.get(email = email)
            if bcrypt.checkpw(password.encode(), signin_user.password.encode()):
                token = jwt.encode({'id': signin_user.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'message': 'SIGN_IN_SUCCESS','TOKEN' : token}, status = 200)
            else:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)
        else:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)
       


    



