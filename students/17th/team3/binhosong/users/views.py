import json
import string

from django.http        import JsonResponse
from django.views       import View

from .models            import Account

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        #for user in data:
        #   if data not in data['user']:
        #       return JsonResponse({'message' : 'data[user]를 입력해주십시오'})

        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message' : '이메일 주소에 \'@\'가 들어가야 합니다.'}, status=400)

        if Account.objects.filter(email = data['email']).exists():
            return JsonResponse({'message' : '이미 존재하는 이메일 입니다.'}, status=400)

        if len(data['password']) < 8:
#            if string.punctuation not in data['password']:
#                return JsonResponse({'message':'특수문자, 영어, 숫자가 포함되야 합니다.'}, status=400)
#            elif string.digits not in data['password']:
#                return JsonResponse({'message':'특수문자, 영어, 숫자가 포함되야 합니다.'}, status=400)
#            elif string.ascii_letters not in data['password']:
#                return JsonResponse({'message':'특수문자, 영어, 숫자가 포함되야 합니다.'}, status=400)
            return JsonResponse({'message' : '비밀번호는 8자 이상으로 설정해주시기 바랍니다.'}, status=400)

        else :
            signup = Account.objects.get_or_create(
                email    = data['email'],
                name     = data['name'],
                nicname  = data['nicname'],
                password = data['password']
        )

        return JsonResponse({'message' : '회원가입 완료'}, status=201)
