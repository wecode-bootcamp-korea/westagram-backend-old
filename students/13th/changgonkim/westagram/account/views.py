#python
import json
#Django
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
#Custom
from account.models import Account

class RegisterView(View):
	def post(self,request):
		#try:
		data 	= json.loads(request.body)
		#Account.objects.create(email=data['email'], username=data['username'], phonenumber=data['phonenumber'], password=data['password'])
		Account(
			email=data['email'], 
			username=data['username'], 
			phonenumber= data['phonenumber'], 
			password=data['password']
		).save()
		return JsonResponse({'MESSAGE': 'Registration Successful'}, status=201)
		#except KeyError:
			#return JsonResponse({'Message': 'hello'}, status=woah)
		#if not email:
		#	return JsonResponse('MESSAGE';'Email is required')
		#elif '@' and '.' not in email:
		#	return JsonResponse('MESSAGE';'Check email format')
		#elif not username:
		#	return JsonResponse('MESSAGE';'Username is required')
		#elif not password:
		#	return JsonResponse('MESSAGE';'Password is required')
		#elif not phonenumber:
		#	return JsonResponse("Phonenumber is required")
		#return JsonResponse({'MESSAGE'; 'Account Created'}, status=201)"""
		#r#########eturn JsonResponse({'message': 'success!'}, status=201)
		##try :
		##	everything
		##except :