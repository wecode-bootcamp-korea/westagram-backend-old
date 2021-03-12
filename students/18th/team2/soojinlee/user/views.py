import json
import bcrypt
import jwt


from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM


class UserSignup(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            user_name    = data['user_name']
            phone_number = data['phone_number']

            repeated_info = User.objects.filter(Q(email=data['email'])
            | Q(user_name=data['user_name']) | Q(phone_number=data['phone_number'])).exists()
        
            if repeated_info:
                return JsonResponse({'message': '이미 있는 정보입니다.'}, status=400)

            if len(password) < 8:
                return JsonResponse({'message': '패스워드는 8자리 이상으로 해야합니다.'}, status=400)

            if '@' not in email or '.' not in email:
                return JsonResponse({'MESSAGE':'유효한 이메일이 아닙니다'}, status=400)
            
            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            User.objects.create(email=email, password=hashed_password.decode('utf-8'), user_name=user_name, phone_number=phone_number)
            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except ValueError :
            return JsonResponse({"message": "사용자계정과 비밀번호를 다시 확인해주세요"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except User.MultipleObjectsReturned:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        


class UserSignin(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            password     = data.get('password')
            user         = data.get('user')

            valid_user = User.objects.get(Q(email=user)| Q(user_name=user) | Q(phone_number=user))

            if valid_user:
                bytes_password = password.encode('utf-8')
                bytes_db_password = valid_user.password.encode('utf-8')

                if bcrypt.checkpw(bytes_password, bytes_db_password):
                    token = jwt.encode({'user_id' : valid_user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse({'access_token': token, 'status':200}, status=200)
                
                else:
                    return JsonResponse({'message' : '비밀번호를 확인하세요'}, status=401)

            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
