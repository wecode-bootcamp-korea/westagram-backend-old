import json
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from .models import SignUp




class SignUpView(View):

	def post(self, request):
		data = json.loads(request.body)

		try:
			if '@' not in data['email'] or '.' not in data['email']:
				return JsonResponse({'MESSAGE' : 'EMAIL_ERROR'}, status=400)

			elif len(data['password']) < 8 :
				return JsonResponse({'MESSAGE' : 'SHORT_PASSWORD'}, status=400)

#elif SignUp.objects.filter(user_name = data['user_name']).exists():
#return JsonResponse({'MESSAGE' : 'USER_NAME_OVERLAP'}, status=400)

#elif SignUp.objects.filter(phone_number = data['phone_number']).exists():
#return JsonResponse({'MESSAGE' : 'PHONE_NUMBER_OVERLAP'}, status=400)

			elif SignUp.objects.filter(email = data['email']).exists():
				return JsonResponse({'MESSAGE' : 'EMAIL_OVERLAP'}, status=400)
	
			else:
				SignUp.objects.create(
#name = data['name'],
#phone_number = data['phone_number'],
					email = data['email'],
#user_name = data['user_name'],
					password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode())
				return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

		except KeyError:
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)



	
class LoginView(View):
	def post(self, request):
		data = json.loads(request.body)

		try : 
			if SignUp.objects.filter(email=data['email']).exists() :
				user = SignUp.objects.get(email=data['email'])
				if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
					return JsonResponse({'MESSAGE' : 'SUCCESS', 'AUTHORIZATION' : jwt.encode({'id':user.id},'helpmeplease', algorithm = 'HS256').decode()}, status = 200) 

				return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)
				
			else :
				return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 401)

		except KeyError:
			return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)





