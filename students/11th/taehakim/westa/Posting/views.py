from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Posting
from .models import Comment
from Account.models import Account
import json

class EnrollPost(View):
    def post(self, request):
        data = json.loads(request.body)
    
        if Account.objects.filter(name = data['user']):
            Posting(
                user      = Account.objects.get(name=data['user']),
                image_url = data['image_url'],
                contents  = data['contents']
            ).save()
            return JsonResponse({"message": 'Success'},   status=200)

class ViewGet(View):
    def get(self, request):
        # res = {
        # 'user':Posting().user,
        # 'time':Posting().time,
        # 'image_url':Posting().image_url,
        # 'contents':Posting.contents
        # }
        res = list(Posting.objects.values())
        return JsonResponse({'post':res},  status=200)

class EnrollComment(View):
    def post(self, requst):
        data = Json.loads(requst.body)
        Comment(
        user_name = data['comment_user'],
        comment   = data['comment'],
        post      = Posting.objects.get(user=data['posting_user'])
        ).save()
        return JsonResponse({"message": 'Success'},   status=200)

class ViewComment(View):
    def get(self, request):
        res = list(Comment.objects.values())
        return JsonResponse({'post':res}, status=200)
