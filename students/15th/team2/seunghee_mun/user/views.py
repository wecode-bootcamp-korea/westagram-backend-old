import json
from django.http     import JsonResponse
from django.views    import View
from user.models import User

class UserView(View):
	def post(self, request):
		data = json.loads(request.body)
		user_info = User.objects.create(
				user_name = date['name'],
				password = date['password'],
				phonenumber = date['H_P'],
				email = date['email']
				)
		return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
