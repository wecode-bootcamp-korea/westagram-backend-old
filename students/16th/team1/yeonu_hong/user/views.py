import json
from django.http  import JsonResponse
from django.views import View
from decorator    import login_check
from .models      import User#, Follow

# 회원가입
class SignUpSignInView(View):
    def post(self, request): 
        try:
            data      = json.loads(request.body)
            name      = data['name']
            phone     = data['phone']
            email     = data['email']
            password  = data['password']

            if User.objects.filter(name=data["name"]):
                name_dup  = User.objects.filter(name=data["name"])
                return JsonResponse({'message': '이미 사용중인 name'}, status=400)
            if User.objects.filter(phone=data["phone"]):
                phone_dup = User.objects.filter(phone=data["phone"])
                return JsonResponse({'message': '이미 사용중인 phone'}, status=400)
            if User.objects.filter(email=data["email"]):
                email_dup = User.objects.filter(email=data["email"])
                return JsonResponse({'message': '이미 사용중인 email'}, status=400)

            if len(password) > 8:
                return JsonResponse({'message': '비밀번호 길이는 8글자 이상'}, status=400)

            User(
                name     = name,
                password = password,
                phone    = phone,
                email    = email).save()
    
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


# # 로그인
# class SignInView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            password  = data['password']

            if 'phone' in data: # 전화번호로 로그인할 경우
                phone = data["phone"]
                if not User.objects.get(phone=data["phone"]):
                    return JsonResponse({'message':'INVALID_USER'}, status=400)
                password_check = User.objects.get(phone=data["phone"]).password
                if password == password_check:
                    return JsonResponse({'message':'SUCCESS'}, status=200)
                else:
                     return JsonResponse({'message':'INVALID_USER'}, status=400)
             
            if 'name' in data: # 이름으로 로그인할 경우
                name = data["name"]
                if not User.objects.get(name=data["name"]):
                    return JsonResponse({'message':'INVALID_USER'}, status=400)
                password_check = User.objects.get(name=data["name"]).password
                if password == password_check:
                    return JsonResponse({'message':'SUCCESS'}, status=200)
                else:
                     return JsonResponse({'message':'INVALID_USER'}, status=400)

            if 'email' in data: # 이메일로 로그인할 경우
                email = data["email"]
                if not User.objects.get(email=data["email"]):
                    return JsonResponse({'message':'INVALID_USER'}, status=400)
                password_check = User.objects.get(email=data["email"]).password
                if password == password_check:
                    return JsonResponse({'message':'SUCCESS'}, status=200)
                else:
                     return JsonResponse({'message':'INVALID_USER'}, status=400)

            return JsonResponse({'message':'KEY_ERROR 비번만넣음'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR 비번없음'}, status=400)


# class FollowView(View):
#     @login_check
#     def post(self, request, user_id):
#         try:
#             data     = json.loads(request.body)
#             user     = User.objects.get(id=user_id)
#             follower = User.objects,get(name=data['user']) # 로그인 하면서 받는 유저


#             if Follow.objects.get(user=user_id):
#                 if Follow.objects.get(user=user_id, follower=follower): # unfollow
#                     pass
#             else:
#                 Follow.objects.create(user=user, follower=follower)
#         except KeyError:
#             return JsonResponse({'message':'KEY_ERROR'}, status=400)   

