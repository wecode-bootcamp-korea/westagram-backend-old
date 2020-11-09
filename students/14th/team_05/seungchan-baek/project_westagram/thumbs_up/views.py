from django.shortcuts import render

from .models import ThumbsUp
from user.models import User
from post.models import Posting

# Create your views here.
import json

from django.views    import View
from django.http     import JsonResponse, request

from .models         import ThumbsUp
from user.models     import User
from post.models     import Posting


class ThumbsUp(View):
    def post(self,  request):
        data = json.loads(request.body)
        user = User.objects.get(id = data['user_id'])
        post = Posting.objects.get(id = data['post_id'])

        ThumbsUp.objects.create(good=data['thumbs'], user=user, post=post)
        return JsonResponse({'message' : "SUCCESS"}, status=201)