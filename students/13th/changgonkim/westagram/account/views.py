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
		if not data.get('email'):
			return JsonResponse({'MESSAGE':'Email required for Registration'}, status=400)
		if not data.get('password'):
			return JsonResponse({'MESSAGE':'Password is required'}, status=400)
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
		#if data['email'] in Account.objects.filter(data['email']) :
			#return JsonResponse({'MESSAGE':'Imposter! Email already exists'})

		#if not password:
			#return JsonResponse({'MESSAGE':'Password is required'})
		Account(
			email=data['email'], 
			username=data['username'], 
			phonenumber= data['phonenumber'], 
			password=data['password']
		).save()
		return JsonResponse({'MESSAGE': 'Registration Successful'}, status=200)
		#except KeyError:
			#return JsonResponse({'Message': 'hello'}, status=woah)
		
		
		#return JsonResponse({'MESSAGE'; 'Account Created'}, status=201)"""
		#r#########eturn JsonResponse({'message': 'success!'}, status=201)
		##try :
		##	everything
		##except :