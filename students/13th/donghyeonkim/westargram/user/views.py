import re
import json
import bcrypt
import jwt

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View
from westargram       import settings 

from user.models      import User

class RegisterView(View):
    def post(self, request):
        user_info = json.loads(request.body)
        name      = user_info['name']
        account   = user_info['account']
        password  = user_info['password']

        if not check_account_password_key(
            account, 
            password):
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, status=400)

        if not account_validation(account):
            return JsonResponse(
                {'MESSAGE':'It doesn\'t fit the email or phone number format.'}, status=400)

        if not password_validation(password):
            return JsonResponse(
                {'MESSAGE':'Password must be at least 8 digits.'}, status=400)

        if account_duplicate_check(account):
            return JsonResponse(
                {'MESSAGE':'This account already exists.'}, status=400)

        if name_duplicate_check(name):
            return JsonResponse(
                {'MESSAGE':'This name already exists.'}, status=400)

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password = password.decode('utf-8')
        User.objects.create(
            name     = name, 
            account  = account,
            password = password)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class LoginView(View):
    def post(self, request):
        user_info = json.loads(request.body)
        account   = user_info['account']
        password  = user_info['password']
        
        if not check_account_password_key(
            account, 
            password):
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, status=400)
        
        account = account_check(account)

        if check_login(account, password):
            access_token = create_token(account)
            return JsonResponse(
                {'MESSAGE': access_token}, status=200)
        else:
            return JsonResponse(
                {'MESSAGE':'INVALID_USER'}, status=401)

class FollowView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        follow_count = user.follows.all().count()
        return JsonResponse({'follow_count':follow_count}, status=200)

    def post(self, request, user_id):
        data    = json.loads(request.body)
        from_user_id = data['user_id']
        to_user_id = user_id

        if int(from_user_id) == int(to_user_id):
            return JsonResponse({'MESSAGE':'자기 자신은 follow 할 수 없습니다.'}, status=200)

        from_user = User.objects.get(pk=from_user_id)
        to_user   = User.objects.get(id=to_user_id)
        
        if from_user in to_user.follows.all():
            to_user.follows.remove(from_user)
            return JsonResponse({'MESSAGE':'follow를 취소했습니다.'}, status=200)
        to_user.follows.add(from_user)
        return JsonResponse({"MESSAGE":"follow를 눌렀습니다."}, status=200)

def check_account_password_key(account, password):
    if account and password:
        return True
    return False

def account_validation(account):
    if bool(
        re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 
        account)):
        return True
    elif bool(
        re.match('^\d{3}-\d{3,4}-\d{4}$', 
        account)):
        return True
    else:
        return False

def password_validation(password):
    if len(password) >= 8:
        return True 
    return False

def account_duplicate_check(account):
    if User.objects.filter(
        Q(account=account)):
        return True
    return False

def name_duplicate_check(name):
    if User.objects.filter(
        Q(name=name)):
        return True
    return False

def account_check(account):
    try:
        account = User.objects.get(account=account).account
    except User.DoesNotExist:
        account = User.objects.get(name=account).account
    return account

def check_login(account, password):
    hashed_password = User.objects.get(account=account).password
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def create_token(account):
    user_id = User.objects.get(account=account).id
    access_token = jwt.encode({'user_id':user_id}, settings.SECRET_KEY, algorithm='HS256')
    access_token = access_token.decode('utf-8')
    return access_token