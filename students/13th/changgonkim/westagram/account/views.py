#python
import json
import bcrypt
import jwt

#Django
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
#Custom
from account.models import Account

class RegisterView(View):
	def post(self,request):
		try:
			data 	= json.loads(request.body)
			#Account.objects.create(email=data['email'], username=data['username'], phonenumber=data['phonenumber'], password=data['password'])

			if '@' not in data['email'] or '.' not in data['email'] :
				return JsonResponse({'MESSAGE':'Check email format. Must include @ and .'})

			if len(data['password']) < 8 :
				return JsonResponse({'MESSAGE':'Password too weak. You are weak. Try again.'})

			if Account.objects.filter(email=data['email']).exists() :
				return JsonResponse({'MESSAGE':'Imposter! Email already exists'})

			if Account.objects.filter(username=data['username']).exists() :
				return JsonResponse({'MESSAGE':'Please be more original with your username'})

			if Account.objects.filter(phonenumber=data['phonenumber']).exists() :
				return JsonResponse({'MESSAGE':'Your phone number is already signed up'})

			hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
			decoded_password = hashed_password.decode('utf-8')

			Account(
				email=data['email'], 
				username=data['username'], 
				phonenumber= data['phonenumber'], 
				password= decoded_password,
			).save()

			return JsonResponse({'message': 'Registration Successful'}, status=200)

		except KeyError:
			return JsonResponse({'key_error':'Check input name or enter all fields'})


class LoginView(View) :
	def post(self,request) :
		data 			= json.loads(request.body)
		try:
			email = data['email']
			password = data['password']

			#if Account.objects.filter(username=data['username']).exists() :
				#user 	 		 = Account.objects.get(username=data['username'])
				#userpassword	 = data['password'].encode('utf-8')
			if Account.objects.filter(email=email).exists():
				user 	 		 = Account.objects.get(email=email)
				userpassword	 = password.encode('utf-8')
				#return JsonResponse({'a': userpassword})

				if bcrypt.checkpw(userpassword, (user.password).encode('utf-8')):
					token = jwt.encode({'id': user.id}, 'secret', algorithm = 'HS256')
					decoded_token = token.decode()
					return JsonResponse({'MESSAGE':'Login_successful', 'user_token' : decoded_token}, status=200)

				else:
					return JsonResponse({'MESSAGE':'Check username and password'}, status=400)
			else:
				return JsonResponse({'MESSAGE':'Username does not exist'}, status=400)

		except KeyError:
			return JsonResponse({'MESSAGE':'Key Error'})
