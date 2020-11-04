import re
import json
import jwt
import bcrypt
from django.http      import JsonResponse 
from django.views     import View  
from user.models      import User, Follow
from django.db.models import Q

class SignupView(View):

    def post(self, request) :
        data        = json.loads(request.body)
        email_check = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-.]{2,3}$')
        phone_check = re.compile('^\d{3}-?\d{3,4}-?\d{4}$')
        
        try :
            if not (data['user_id'] and data['password'] and data['user_name']) :
                return JsonResponse({'MESSAGE':'No Value'}, status=400)
            elif not re.match('.{8}',data['password']) :
                return JsonResponse({'MESSAGE':'Password too short'}, status=400)
        except KeyError as e:
            return JsonResponse({'Key_Error':str(e)}, status=400)
        hashed_password  = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf-8')
        try :
            new_user     = User(name = data['name'], password  = decoded_password)
        except KeyError :
            new_user     = User(password  = decoded_password)

        if email_check.match(data['user_id']) :
            if User.objects.filter(Q(user_name = data['user_name']) | Q(email = data['user_id'])).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                new_user.user_name = data['user_name']                
                new_user.email     = data['user_id']
                new_user.save()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        elif phone_check.match(data['user_id']):
            phone_number = ''.join(data['user_id'].split('-'))
            if User.objects.filter(Q(user_name = data['user_name']) | Q(phone_number = phone_number)).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                new_user.user_name    = data['user_name']
                new_user.phone_number = phone_number
                new_user.save()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        else :
            return JsonResponse({'MESSAGE':'Invalid email address or phone number'}, status=400)

class LoginView(View):
    def __init__(self):
        self.SECRET = 'secret'

    def post(self, request) :
        data = json.loads(request.body)
        try :
            phone_number = ''.join(data['user_id'].split('-'))
            if not (data['user_id'] and data['password']) :
                return JsonResponse({'MESSAGE':'No Value'}, status=400)
        except KeyError as e:
            return JsonResponse({'Key_Error':str(e)}, status=400)
        try :    
            user1 = User.objects.get(Q(user_name = data['user_id']) | Q(email = data['user_id']) | Q(phone_number = data['user_id']))
            if bcrypt.checkpw(data['password'].encode('utf-8'), user1.password.encode('utf-8')):
                access_token = jwt.encode({'id' : user1.id}, self.SECRET, algorithm = 'HS256')
                return JsonResponse({'MESSAGE':'SUCCESS','token':access_token.decode('utf-8')}, status=201)
            else : 
                return JsonResponse({"MESSAGE": "WRONG PASSWORD"}, status=401)
        except User.DoesNotExist : #DoesNotExist 오류를 잡을땐 테이블명을 적어 줘야함
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401) 

    #토큰 받기 테스트
    def get(self, request) :
        encoded_token = request.headers['token'].encode('utf-8')
        user_id = jwt.decode(encoded_token, self.SECRET, algorithm='HS256')
        print(user_id['id'])
        return JsonResponse({'user_id':user_id.get('id')}, status=201)

class FollowView(View):

    def post(self, request) :
                
        data = json.loads(request.body)
        user_id = User.objects.get(id = data['user_id'])
        followee_id = User.objects.get(id = data['followee_id'])
        follow_check = Follow.objects.filter(Q(follower=user_id) & Q(followee=followee_id))
        if follow_check :
            follow_check.delete()
            return JsonResponse({'MESSAGE':'Follow_cancel'}, status=201)
        else :
            Follow.objects.create(follower=user_id,followee=followee_id)
            return JsonResponse({'MESSAGE':'Follow_success'}, status=201)


