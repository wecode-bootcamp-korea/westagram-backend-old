import json
import re
from django.http     import JsonResponse
from django.views    import View
from django.core.exceptions import ValidationError
from user.models import User

class UserView(View):
	def post(self, request):
		data = json.loads(request.body)
		user_email = re.match('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{3})$', data['name'])
		user_HP    = re.match('^[0-9]{3}-[0-9]{4}-[0-9]{4}$', data['name'])
		user_id    = re.match('^[a-z0-9_-]{2,10}$', data['name'])
		password   = re.match('^\w{8, 15}$', data['password'])
		
		#Key validtion
		if not user_email and not user_HP and not user_id:
			return JsonResponse({"message": "KEY_ERROR"}, status=400)	
	
		# email validtion
		if data['name'] == user_email:
			return JsonResponse({'MESSAGE' : 'EMAIL_ERROR'}, status=400)

	
		# name validtion
		if  data['name'] == user_id:
			return JsonResponse({'MESSAGE' : 'NAME_ERROR'}, status=400)	
		
		# HP validion
		if  data['name'] == user_HP:
			return JsonResponse({'MESSAGE' : 'HP_ERROR'}, status=400)
		
		# password validtion
		if  data['password'] == password:
			return JsonResponse({'MESSAGE' : 'PW_ERROR'}, status=400)
	
		# info_overlap
		if not User.objects.filter(user_name=data['name']):
			User.objects.create(user_name=data['name'], password=data['password'])
			return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
		return JsonResponse({'MESSAGE' : 'INFO_OVERLAP_ERROR'}, status=400)

	def get(self, request):
		get_data = json.loads(request.body)

		# Key_error
		try:
			get_user_name = get_data['name']
			get_password  = get_data['password']	
		except:
			return JsonResponse ({'message': 'KEY_ERROR'}, status=400)

		# Invalid_user
		if not User.objects.filter(user_name=get_data['name']) or not User.objects.filter(password=get_data['password']):
			return JsonResponse({"message": "INVALID_USER"}, status=401)
		return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)	 

		
			
