import json
import re

from django.views import View
from django.http import JsonResponse
from user.models import Account

class UserView(View):
	def post(self, request):
		data = json.loads(request.body)

		if (data['email'] == '') and (data['name'] == '') and (data['phone'] == ''):
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

		p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		if p.match(data['email'] != None) == False:
			return JsonResponse({'MESSAGE':'EMAIL_VALIDATION'}, status = 400)

		if Account.objects.filter(name = data['name']).exists() and (data['name'] != ''):
			return JsonResponse({'MESSAGE':'NAME_DUPLICATED'}, status = 400)

		if Account.objects.filter(email = data['email']).exists() and (data['email'] != ''):
			return JsonResponse({'MESSAGE':'EMAIL_DUPLICATED'}, status = 400)

		if Account.objects.filter(phone = data['phone']).exists() and (data['phone'] != ''):
			return JsonResponse({'MESSAGE':'PHONE_DUPLICATED'}, status = 400)

		if (data['email'] == '') or (data['password'] == ''):
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

		if (len(data['password']) < 8):
			return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION'}, status = 400)

		name = Account.objects.create(
			name = data['name'], email = data['email'], phone = data['phone'], password = data['password']
		)

		return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

	def get(self, request):
		account_data = Account.objects.values()
		return JsonResponse({'account':list(account_data)}, status = 200)
