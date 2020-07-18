import json
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class LoginView(View):
	def post(self, request):
		#입력받은 데이터들
		data = json.loads(request.body)
		try:
			if Users.objects.filter(email=data['email']).exists():
				user = Users.objects.get(email=data['email'])
				if data['password'] == user.password:
					return JsonResponse({'message':'SUCCESS'}, status = 200)
				return JsonResponse({'message':'WRONG'},status=401)

			return JsonResponse({'message':'USER No'}, status = 400)
		except KeyError:
			return JsonResponse({'message':'INVALID_KEY'}, status = 400)
		

	

		

		
class SignUpView(View):
	def post(self, request):
		data = json.loads(request.body)
		print("request.body:", request.body)

		Users(
#name = data['name'],
			name = "lee",
			email = data['email'],
			password = data['password']
			).save()

		return JsonResponse({'message':'SUCCESS'}, status=200)

	def get(self, request):
		return JsonResponse({"Hello":"World"}, status=200)




       

