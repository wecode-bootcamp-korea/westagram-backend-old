import json, re, bcrypt, jwt

from django.views import View
from django.http import JsonResponse

from project_westagram.settings import SECRET_KEY
from user.models import Account, Relation

class SignUpView(View): #회원가입
	def post(self, request):
		data = json.loads(request.body)

		if (data['email'] == '') and (data['phone'] == ''):
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

		if data['password'] == '' or data['name'] == '':
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

		p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		if data['email'] != '' and (p.match(str(data['email'])) != None) == False:
			return JsonResponse({'MESSAGE':'EMAIL_VALIDATION'}, status = 400)

		if Account.objects.filter(name = data['name']).exists() and (data['name'] != ''):
			return JsonResponse({'MESSAGE':'NAME_DUPLICATED'}, status = 400)
		elif Account.objects.filter(email = data['email']).exists() and (data['email'] != ''):
			return JsonResponse({'MESSAGE':'EMAIL_DUPLICATED'}, status = 400)
		elif Account.objects.filter(phone = data['phone']).exists() and (data['phone'] != ''):
			return JsonResponse({'MESSAGE':'PHONE_DUPLICATED'}, status = 400)

		if (len(data['password']) < 8):
			return JsonResponse({'MESSAGE':'PASSWORD_VALIDATION'}, status = 400)

		password = data['password']
		hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		Account.objects.create(
			name 	 = data['name'], 
			email 	 = data['email'], 
			phone 	 = data['phone'], 
			password = hashed_pw.decode('utf-8')
		)

		return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

	def get(self, request):
		account_data = Account.objects.values()
		return JsonResponse({'account':list(account_data)}, status = 200)

class SignInView(View): #로그인
	def post(self, request):
		data = json.loads(request.body)
		password = data['password']
		account  = data['account']

		if account == '' or password == '':
			return JsonResponse({'MESSAGE':'KEY_ERROR'}, status = 400)

		if Account.objects.filter(email = account).exists():
			account_data = Account.objects.get(email = account)

			if bcrypt.checkpw(password.encode('utf-8'), account_data.password.encode('utf-8')) == False:
				return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)

			access_token = jwt.encode({'email': account}, SECRET_KEY, algorithm = 'HS256')

		elif Account.objects.filter(phone = account).exists():
			account_data = Account.objects.get(phone = account)

			if bcrypt.checkpw(password.encode('utf-8'), account_data.password.encode('utf-8')) == False:
				return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)
			
			access_token = jwt.encode({'phone': account}, SECRET_KEY, algorithm = 'HS256')

		elif Account.objects.filter(name = account).exists():
			account_data = Account.objects.get(name = account)

			if bcrypt.checkpw(password.encode('utf-8'), account_data.password.encode('utf-8')) == False:
				return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)

			access_token = jwt.encode({'name': account}, SECRET_KEY, algorithm = 'HS256')
			
		else:
			return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 401)

		return JsonResponse({'MESSAGE':'SUCCESS', 'token':access_token.decode('utf-8')}, status = 200)

class FollowAccount(View): # 팔로우 등록
	def post(self, request):
		data = json.loads(request.body)

		if Relation.objects.filter(from_account = data['from_account_id'], to_account = data['to_account_id']).exists():
				follow = Relation.objects.filter(from_account = data['from_account_id'], to_account = data['to_account_id'])
				follow.delete()
		else:
			Relation.objects.create(
				from_account = Account(id = data['from_account_id']),
				to_account   = Account(id = data['to_account_id'])
			)

		from_followees = Relation.objects.filter(from_account = data['from_account_id']).count()
		to_followers   = Relation.objects.filter(to_account = data['to_account_id']).count()

		from_account = Account.objects.filter(id = data['from_account_id']).get()
		from_account.followees = from_followees
		from_account.save()

		to_account = Account.objects.filter(id = data['to_account_id']).get()
		to_account.followers = to_followers
		to_account.save()

		return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)
		
