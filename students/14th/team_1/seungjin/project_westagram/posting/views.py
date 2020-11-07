import json
import re
from django.db.models import Q
from django.core import serializers
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .models import (
                    Posts,
                    Comments,
                    Likes,
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
        try:
            data    = json.loads(request.body)
        except Exception as ex:
            return JsonResponse({"message":"You request with wrong format."}, status=400)
        
        # image_url, user account 정보를 추출하여 posts table에 추가 작업
        keys        = ['account', 'image_url', 'article'] 
        inputs      = {k:v for k,v in data.items() if k in keys}
        
        for key in keys:
            if not key in inputs:
                return JsonResponse({"message":"we need to take all values [account, image_url, article]"}, status=400)
        
        user_id     = getUserID(inputs['account'])

        Posts.objects.create(
                        article     = inputs['article'], 
                        image_url   = inputs['image_url'],
                        created_at  = datetime.now(), 
                        user        = user_id
                        ) 
        return JsonResponse({"message":"SUCCESS"}, status=201)

class ShowAllPosts(View):
    def get(self, request):
        #posts = serializers.serialize('json', Posts.objects.all(), fields=('article', 'image_url', 'created_at'))

        posts       = []
        entries     = Posts.objects.select_related('user').all()
        
        for row in entries:
            posts.append({"article":row.article, "image_url":row.image_url, "created_at":row.created_at ,"user":row.user.name})
        
        return JsonResponse({"posts":posts}, status=200)

class AddComment(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
        except Exception as ex:
            return JsonResponse({"message":"You request with wrong format."}, status=400)
        
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
        entries     = Comments.objects.select_related('user', 'post').all()
        comments    = []
        for row in entries:
            comments.append({'article':row.article, 'created_at':row.created_at,
                            'user':row.user.name, 'post':row.post.id})
        
        return JsonResponse({"comments":comments}, status=200)

class ShowCommentsOfPost(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
        except Exception as ex:
            return JsonResponse({"message":"You request with wrong format."}, status=400)

        post_id     = ''
       
        if "post_id" in data:
            post_id = data['post_id']
        else:
            return JsonResponse({"message":"post_id is empty"}, status=400)

        comments    = []
        entries     = Comments.objects.select_related('user', 'post').filter(post_id=post_id)
        
        for row in entries:
            comments.append({'article':row.article, 'created_at':row.created_at,
                            'user':row.user.name, 'post':row.post.id})
        
        return JsonResponse({"comments":comments}, status=201)        

'''
class AddLike(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # '좋아요' 대상 post, comment 와 사용자정보
'''     



