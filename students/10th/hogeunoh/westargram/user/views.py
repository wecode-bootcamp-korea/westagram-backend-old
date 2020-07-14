import json

from django.views	import View
from django.http	import JsonResponse

from .models		import Users

class SignUp(View):
	def post(self, request):
		data = json.loads(request.body)
		check = Users.objects.filter(email = data['email']).exists()
		try:
			if check:
				return JsonResponse({'message':'email중복'}, status=401)
			else:
				Users(
					name		=data['name'],
					email		=data['email'],
					password	=data['password']
				).save()
				return JsonResponse({'message':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'message':'KEY_ERROR'}, status=400)

	def get(self, request):
		return JsonResponse({'회원가입' : '!!'}, status=200)


class SignIn(View):
	def post(self, request):
		data = json.loads(request.body)
		user = Users.objects.get(email=data['email'])
		try:
			if user and user.password == data['password']:
				return JsonResponse({'message':'SUCCESS'}, status=200)
		except KeyError:
			return JsonResponse({'error':'KEY_ERROR'}, status=400)
		return JsonResponse({'message':'INVALID_USER'}, status=401)

