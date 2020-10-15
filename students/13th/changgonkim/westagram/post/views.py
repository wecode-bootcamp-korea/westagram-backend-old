#python
import json
import bcrypt
import jwt

#Django
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
#Custom
from post.models import Posting
from account.models import Account

class PostView(View) :
	def post(self,request) :
		try:
			data	= json.loads(request.body)
			user		= Account.objects.get(id=data['userid'])
			image_url	= data['imageurl']
			caption		= data['caption']
			Posting.objects.create(
				poster		= user,
				imageurl	= imageurl,
				caption		= caption,
				)
			return JsonResponse({'message':'Post successful'})

		except KeyError:
			return JsonResponse({'key error':'must add posterid and image url'})

class ReadView(View) :
	def get(self, request) :
		print('1')
		posts	= Posting.objects.all().values()
		postfeed= [post for post in posts]
			#postfeed.append(post)
		print('2')
		return JsonResponse({'all posts': postfeed})
