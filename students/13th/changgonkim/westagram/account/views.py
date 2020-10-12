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
		data = json.loads(request.body)
		account = Account.objects.create(email=data['email'], username=data['username'], phonenumber=data['phonenumber'], password=data['password'])
		return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)