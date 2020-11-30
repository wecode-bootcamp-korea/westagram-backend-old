import json
from django.http        import JsonResponse
from django.views       import View
from .models            import Users
from django.db.models   import Q

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        
        Users(
            name        = data['name'],
            email       = data['email'], 
            password    = data['password'],
        )
        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message':'EMAIL VALIDATION'},status =400)        
        
        if len(data['password']) < 8:
            return JsonResponse({'message':'PASSWORD VALIDATION'},status=400)
        
        if Users.objects.filter(name = data['name']).exists() == True:
            return JsonResponse({'message' : '이미 존재하는 아이디입니다.'},status=401)
        else:
            try:
                Users.objects.create(name = data['name'], email = data['email'], password = data['password'])
                return JsonResponse({'message': '회원가입완료'},status=200)
            
            except Exception as e:
                print(e)
        
class Login(View):
    def post(self,request):
        data = json.loads(request.body)
        print('a')
        
        # Users(
        #     name        = data['name'],
        #     email       = data['email'], 
        #     password    = data['password'],
        # )
        
        try:
            login_info = Users.objects.filter(Q(name = data['name']) & Q(email = data['email']) & Q(password=data['password']))
            if login_info.exists():
                return JsonResponse({'message':'로그인 성공'},status=200)
            else:
                return JsonResponse({'message':'아이디가 존재하지 않습니다.'},status=401)

        
        # except Users.DoesNotExist:
            # return JsonResponse({'message':'아이디가 존재하지 않습니다.'},status=401)

        except Exception as e:
            return JsonResponse({'d':f'{e}'},status=400)
        
    
            # User.object.filter(name = data['name'], password = data['password']).exists() == True:
            
            # if Users.objects.filter(name = data['name']).exists():
            #     user = Users.objects.get(name = data['name'], password = data['password'])

            #     if user.password == data['password']:
            #         return JsonResponse({'message':'로그인 성공'},status=200)
            #     else:
            #         return JsonResponse({'message':'비밀번호 불일치'},status=401)
                
            # return HttpResponse(status=400)

                      
            # if user.values('password') == data['password']):
            #     return JsonResponse({'message': '로그인완료'},status=200)
            # else:
            #     return JsonResponse({'message': '비밀번호가 다릅니다'},status=200)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users':list(user_data)},status=200)
