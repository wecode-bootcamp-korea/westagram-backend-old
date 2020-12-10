
import json, re
import bcrypt
import jwt

from django.http        import JsonResponse
from django.views       import View
from django.db          import IntegrityError
from django.db.models   import Q

from user.models        import User



class UserView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            data['name']    =   data.get('name')
            data['email']   =   data.get('email')
            data['mobile_number']   =   data.get('mobile_number')

            if len(data['password']) < 8:
                return JsonResponse({"message":"password must be at least 8 characters"},status=400)

            email_reg='[a-zA-Z0-9_-]+@[a-z]+.[a-z]'
            email_validation = re.compile(email_reg)

            if 'email' in data:
                if re.match(email_validation, str(data.get('email'))):
                    return JsonResponse({"message":"it is not a vaild address"},status = 400)

            if User.objects.filter(Q(name=data['name']) & Q(email=data['email']) & Q(mobile_number=data['mobile_number'])).exists():
                return JsonResponse({'message': 'It is already_exist'}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            password= hashed_password.decode('utf-8')

            User.objects.create(
                name         = data['name'] ,
                mobile_number = data['mobile_number'] ,
                email        = data['email'] ,
                password     = password,
                )

            return JsonResponse({'message' : 'SUCCESS'}, status=200)
        except IntegrityError:
            return JsonResponse(stats=400)

    def get(self,request):
        user_data = list(User.objects.values())
        try:
            return JsonResponse({'data':user_data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'ACCOUNT_DOES_NOT_EXIST'}, status=400)


class SigninView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            data['name']    = data.get('name')
            data['mobile_number'] = data.get('mobile_number')
            data['email'] = data.get('email')
            user_password = data.get('password')
            SECRET = 'wecode'

            if data['name'] is None and data['mobile_number'] is None:
                if User.objects.filter(email=data['email']).exists():
                    user = User.objects.get(email=data.get('email'))
                    if bcrypt.checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({"name":data['name']},SECRET,algorithm = "HS256")
                        return JsonResponse({'token':token.decode('utf-8')}, status = 200)
                    return JsonResponse({"message":"password is not valid"},status =400)

            #번호만 잇는 경우
            if data['name'] is None and data['email'] is None:
                if User.objects.filter(mobile_number=data.get("mobile_number")).exists():
                    user = User.objects.get(mobile_number= str(data['mobile_number']))
                    if bcrypt.checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({"name":data['name']},SECRET,algorithm = "HS256")
                        return JsonResponse({'token':token.decode('utf-8')}, status = 200)
                    return JsonResponse({"message":"password is not valid"},status =400)

            # 이름만 잇는 경
            if data['mobile_number'] is None and data['email'] is None:
                if User.objects.filter(name= data['name']).exists():
                    user = User.objects.get(name=data['name'])
                    if bcrypt.checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({"name":data['name']},SECRET,algorithm = "HS256")
                        return JsonResponse({'token':token.decode('utf-8')}, status = 200)
                    return JsonResponse({"message":"password is not valid"},status =400)

        except KeyError as e:
                    return JsonResponse({"message":e.message},status=400)


