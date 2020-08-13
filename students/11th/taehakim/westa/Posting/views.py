from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Posting
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
        res2 = list(Posting.objects.values())
        return JsonResponse({'post':res2},  status=200)
    