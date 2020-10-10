import json
import re

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
        
        if password == '' or email == '':
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        if len(password)<8: 
            return JsonResponse({'message': 'PASSWORD IS NOT VALID'}, status=400)

        if re.match(email_pattern, email) == None:
            return JsonResponse({'message': 'EMAIL IS NOT VALID'}, status=400)

        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists(): 
            return JsonResponse({'message': 'USER ALREADY EXISTS'}, status=400)
        
        User.objects.create(
            email    = email,
            name     = name,
            password = password,
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
        data=json.loads(request.body)
        # 팔로우 하는 사람(follower)의 user_id를 입력받음
        follower=data['user_id']
        follower_obj=get_object_or_404(User, pk=follower)
        user=User.objects.filter(id=user_id)
        
        # 요청한 user_id가 전체 유저의 수보다 크면 에러를 반환
        if int(user_id)>User.objects.all().count():
            return JsonResponse({'message':'USER DOES NOT EXIST'}, status=404)
        else:
            follower_obj.follow.add(user_id)
            return JsonResponse({'message': 'FOLLOWED'}, status=201)
         
        
        # get으로 불러와서 DoesNotExist에러가 뜨면 에러 메시지를 리턴하도록 했으나 실패
        '''
        try:
            if User.objects.filter(id=user_id)=='<QuerySet []>':
                raise DoesNotExist
            follower_obj.follow.add(user_id)
            return JsonResponse({'message': 'FOLLOWED'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'USER DOES NOT EXIST'}, status=404)
        '''