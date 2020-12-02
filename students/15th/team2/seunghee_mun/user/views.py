import json
from django.http     import JsonResponse
from django.views    import View
from django.core.exceptions import ValidationError
from user.models import User

class UserView(View):
	def post(self, request):
		data = json.loads(request.body)
		print(data)
		if not data['email'] or not data['password']:
			return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
	
		if not '@' in data['email'] or not '.' in data['email']:
			return JsonResponse({'MESSAGE' : 'NOT EMAIL FORM'}, status=400)

		user_info = User.objects.create(user_name = data['name'],
						password = data['password'],
						phonenumber = data['HP'],
						email = data['email'])
		return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
