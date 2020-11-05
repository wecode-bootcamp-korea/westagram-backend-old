import json
import re
from django.core import serializers
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .models import (
                    Posts,
                    Comments,
                    )
from user.models import Users

def getUserID(user_input):
    return Users.objects.get(
                        Q(name          = user_input)|
                        Q(phone_number  = user_input)|
                        Q(email         = user_input)
                        ).id
    

class Posting(View):
    def post(self, request):
        data    = json.loads(request.body)
        
        # image_url, user account 정보를 추출하여 posts table에 추가 작업
        keys    = ['account', 'image_url', 'article'] 
        
        # dictionary conprehension 시도해보기
        inputs  = {k:v for k,v in data.items() if k in keys}
        
        '''
        inputs  = {}
        for key in keys:
            if key in data:
                inputs[key] = data[key]
            else:
                inputs[key] = ''
        '''
        
        if not 'account' in data:
            return JsonResponse({"message":"account info to posting is empty."}, status=400)
        
        if not 'image_url' in data:
            data['image_url']   = ''
        
        if not 'article' in data:
            data['article']     = ''
        
        '''
        user = Users.objects.get(
                            Q(name          = inputs['account'])|
                            Q(phone_number  = inputs['account'])|
                            Q(email         = inputs['account'])
                            )
        '''
        user_id     = getUserID(inputs['account'])

        Posts.objects.create(
                        article     = inputs['article'], 
                        image_url   = inputs['image_url'],
                        created_at  = datetime.now(), 
                        user_id     = user_id
                        ) 

        return JsonResponse({"message":"SUCCESS"}, status=201)

class ShowAllPosts(View):
    def get(self, request):
        posts = serializers.serialize('json', Posts.objects.all())
        return JsonResponse({"posts":posts}, status=200)

class AddComment(View):
    def post(self, request):
        data        = json.loads(request.body)
        inputs      = {}
        
        ARTICLE     = 'article'
        ACCOUNT     = 'account'
        POST_ID     = 'post_id'

        # article, user_id, post_id, created_at 에 대해 comments table에 추가.
        if ACCOUNT in data:
            inputs[ACCOUNT] = data[ACCOUNT]
        else:
            return JsonResponse({"message":"user info to comment is empty."}, status=400) 
        
        if ARTICLE in data:
            inputs[ARTICLE] = data[ARTICLE]
        else:
            return JsonResponse({"message":"Can't comment empty article."}, status=400) 

        if POST_ID in data:
            inputs[POST_ID] = data[POST_ID]
        else:
            return JsonResponse({"message":"post_id is empty."}, status=400) 

        user_id     = getUserID(inputs[ACCOUNT])

        Comments.objects.create(
                            user_id     = user_id,
                            article     = inputs[ARTICLE],
                            post_id     = inputs[POST_ID],
                            created_at  = datetime.now()
                            )

        return JsonResponse({"message":"SUCCESS"}, status=201)
            

class ShowAllComments(View):
    def get(self, request):
        comments = serializers.serialize('json', Comments.objects.all())
        
        return JsonResponse({"comments":comments}, status=200)

class ShowCommentsOfPost(View):
    def post(self, request):
        data     = json.loads(request.body)
        post_id  = ''
       
        if "post_id" in data:
            post_id = data['post_id']
        else:
            return JsonResponse({"message":"post_id is empty"}, status=400)

        comments = serializers.serialize('json', 
                                    Comments.objects.filter(post_id = post_id))

        return JsonResponse({"comments":comments}, status=201)        








