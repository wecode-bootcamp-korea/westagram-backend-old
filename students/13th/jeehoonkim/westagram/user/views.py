import json
import re
import bcrypt

from django.views     import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http      import JsonResponse

from .models          import User

class SignUpView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        name     = data['name']
        password = data['password']
        phone    = data['phone']

        email_pattern = '^\w+([-_.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        # 8자 이상, 최소 하나의 문자, 숫자, 특수문자
        password_pattern = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        
        if password == '' or email == '':
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        if re.match(password_pattern, password) == None: 
            return JsonResponse({'message': 'PASSWORD IS NOT VALID'}, status=400)
        
        if re.match(email_pattern, email) == None:
            return JsonResponse({'message': 'EMAIL IS NOT VALID'}, status=400)

        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists(): 
            return JsonResponse({'message': 'USER ALREADY EXISTS'}, status=400)
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        #return JsonResponse({'ee':f"{hashed_password}"})
        User.objects.create(
            email    = email,
            name     = name,
            password = hashed_password,
            phone    = phone
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class SignInView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        phone    = data['phone']
        
        if (phone or email) and password:
           try:
                User.objects.get(Q(phone=phone) | Q(email=email), password=password)
           except User.DoesNotExist:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
           else:
                return JsonResponse({'message': 'SUCCESS'}, status=200)
        else:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class FollowView(View):
    # 팔로우 할 사람의 user_id가 url에 있음
    def post(self, request, user_id):
        data         = json.loads(request.body)
        # 팔로우 하는 사람(follower)의 user_id를 입력받음
        follower     = data['user_id']
        follower_obj = get_object_or_404(User, pk=follower)
        
        followed=User.objects.get(id=user_id)
        # 모든 유저의 id를 호출해서 입력받은 id와 비교. id가 없다면 에러 메시지 반환
        for i in range(User.objects.all().count()):
            if int(user_id) == list(User.objects.all().values('id'))[i]['id']:
                if followed in follower_obj.follow.all():
                    follower_obj.follow.remove(user_id)
                    return JsonResponse({'message': 'UNFOLLOWED'})
                else:
                    follower_obj.follow.add(user_id)
                    return JsonResponse({'message': 'FOLLOWED'}, status=201)
                
        else:
            return JsonResponse({'message':'USER DOES NOT EXIST'}, status=404)
         
        
        # get으로 불러와서 DoesNotExist에러가 뜨면 에러 메시지를 리턴하도록 했으나 실패
        #filter로 불러와서 빈 리스트이면 에러 메시지를 리턴하도록 했으나 실패
        '''
        try:
            if User.objects.filter(id=user_id)=='<QuerySet []>':
                raise DoesNotExist
            follower_obj.follow.add(user_id)
            return JsonResponse({'message': 'FOLLOWED'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'USER DOES NOT EXIST'}, status=404)
        '''