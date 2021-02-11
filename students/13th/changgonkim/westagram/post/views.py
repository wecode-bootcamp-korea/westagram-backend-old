#python
import json
import bcrypt
import jwt

#Django
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
#Custom
from post.models import Posting, Comment
from account.models import Account

class PostView(View) :
	def post(self,request) :
		try:
			data		= json.loads(request.body)
			user		= Account.objects.get(id=data['userid'])
			image_url	= data['imageurl']
			caption		= data['caption']

			Posting.objects.create(
				poster		= user,
				imageurl	= image_url,
				caption		= caption,
			)

			return JsonResponse({'message':'Post successful'}, status=200)

		except KeyError:
			return JsonResponse({'key error':'must add posterid and image url'})


class ReadView(View) :
	def get(self, request) :
		posts	= Posting.objects.all().values()
		postfeed= [post for post in posts]
		return JsonResponse({'all posts': postfeed})


class CommentView(View) :
	def post(self, request) :
		try:
			data 	= json.loads(request.body)
			post 	= Posting.objects.get(id=data['post'])
			user 	= Account.objects.get(id=data['user'])
			comment = data['comment']
			
			Comment.objects.create(
				commented_post 	= post,
				commenter 		= user,
				comment 		= comment,
			)
			print(data)
			return JsonResponse({'message':'Such success!'}, status=200)
			
		except KeyError:
			return JsonResponse({'key error: No comment entered'})

	def get(self,request) :
		data	 = json.loads(request.body)
		post 	 = Comment.objects.filter(commented_post=data['post']).values()
		comments = [comments for comments in post]
		return JsonResponse({'all comments for post': comments}, status=200)