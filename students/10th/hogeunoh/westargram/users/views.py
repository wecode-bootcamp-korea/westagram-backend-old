import json, bcrypt, jwt

from django.views			import View
from django.http			import JsonResponse

from .models				import Users
from westargram.settings 	import SECRET_KEY, ALGORITHM

class SignUp(View):
	def post(self, request):
		data = json.loads(request.body)
		check = Users.objects.filter(email = data['email']).exists()
		try:
			if check:
				return JsonResponse({'message':'email중복'}, status=401)
			else:
				Users(
					email		= data['email'],
					password	= bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#					password	=data['password']
				).save()
				return JsonResponse({'message':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'message':'KEY_ERROR'}, status=400)

	def get(self, request):
		return JsonResponse({'회원가입' : '!!'}, status=200)


class SignIn(View):
	def post(self, request):
		data = json.loads(request.body)
		user = Users.objects.filter(email=data['email'])
		try:
			if user and bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):
				token = jwt.encode({'user': user[0].id}, SECRET_KEY, ALGORITHM).decode('utf-8')
				return JsonResponse({'message':token}, status=200)
			else:
				return JsonResponse({'message':'INVALID_USER'}, status=401)
		except KeyError:
			return JsonResponse({'error':'KEY_ERROR'}, status=400)
