import json

from django.views import View
from django.http import JsonResponse
from user.models import Account

class UserView(View):
	def post(self, request):
		data = json.loads(request.body)
		
		name = Account.objects.create(
			name=data['name'], email=data['email'], phone=data['phone'], password=data['password']
		)

		return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

	def get(self, request):
		account_data = Account.objects.values()
		return JsonResponse({'account':list(account_data)}, status=200)
