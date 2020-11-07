import json
import re
from django.db.models import Q
from django.core import serializers
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from share.utils import (
                        getUserID,
                        checkRequestBody,
                        )
from .models import (
                    Posts,
                    Comments,
                    Contents,
                    Likes,
                    )
from user.models import Users

class Posting(View):
    def post(self, request):
        checkRequestBody(request)
        data = json.loads(request.body)

        # image_url, user account 정보를 추출하여 posts table에 추가 작업
        keys        = ['account', 'image_url', 'article'] 
        inputs      = {k:v for k,v in data.items() if k in keys}
        
        for key in keys:
            if not key in inputs:
                return JsonResponse({"message":"we need to take all values [account, image_url, article]"}, status=400)
        
        user_id     = getUserID(inputs['account'])

        Contents.objects.create(
                        article     = inputs['article'], 
                        created_at  = datetime.now(), 
                        user_id     = user_id
                        )
        Posts.objects.create(
                        image_url   = inputs['image_url'],
                        content_id  = Contents.objects.last().id
                        )

        return JsonResponse({"message":"SUCCESS"}, status=201)


class ShowAllPosts(View):
    def get(self, request):
        posts       = []
        entries     = Posts.objects.select_related('content').select_related('content__user').all()
        
        for row in entries:
            posts.append({"article":row.content.article, "image_url":row.image_url, "created_at":row.content.created_at , "user":row.content.user.name})
        
        return JsonResponse({"posts":posts}, status=200)

class AddComment(View):
    def post(self, request):
        checkRequestBody(request)
        data = json.loads(request.body)
        
        inputs      = {}
        ARTICLE     = 'article'
        ACCOUNT     = 'account'
        CONTENT_ID  = 'content_id'

        # article, user_id, post_id, created_at 에 대해 comments table에 추가.
        if ACCOUNT in data:
            inputs[ACCOUNT] = data[ACCOUNT]
        else:
            return JsonResponse({"message":"user info to comment is empty."}, status=400) 
        
        if ARTICLE in data:
            inputs[ARTICLE] = data[ARTICLE]
        else:
            return JsonResponse({"message":"Can't comment empty article."}, status=400) 

        if CONTENT_ID in data:
            inputs[CONTENT_ID] = data[CONTENT_ID]
        else:
            return JsonResponse({"message":"post_id is empty."}, status=400) 

        user_id     = getUserID(inputs[ACCOUNT])
        
        if user_id == None:
            return JsonResponse({"message":"Can't find user."}, status=400)

        Contents.objects.create(
                        article     = inputs[ARTICLE], 
                        created_at  = datetime.now(), 
                        user_id     = user_id
                        )
        
        if Comments.objects.filter(content_id=inputs[CONTENT_ID]).exists():
            inputs['parent_comment_id'] = inputs[CONTENT_ID]
        else:
            inputs['parent_comment_id'] = None

        
        Comments.objects.create(
                            content_id          = Contents.objects.last().id,
                            parent_comment_id   = inputs["parent_comment_id"],  
                            )

        return JsonResponse({"message":"SUCCESS"}, status=201)
            

class ShowAllComments(View):
    def get(self, request):
        entries     = Comments.objects.select_related('content').select_related('content__user').all()
        comments    = []
        for row in entries:
            comments.append({'article':row.content.article, 'created_at':row.content.created_at,
                            'user':row.content.user.name})
        
        return JsonResponse({"comments":comments}, status=200)

class ShowCommentsOfContent(View):
    def post(self, request):
        checkRequestBody(request)
        data       = json.loads(request.body)
        content_id = None
       
        if "content_id" in data:
            content_id = data['content_id']
        else:
            return JsonResponse({"message":"content_id is empty"}, status=400)

        comments    = []
        entries     = Comments.objects.select_related('content').filter(content_id=content_id)
        
        for row in entries:
            comments.append({'article':row.content.article, 'created_at':row.content.created_at,
                            'user':row.content.user.name})
        
        return JsonResponse({"comments":comments}, status=201)        

class AddLike(View):
    def post(self, request):
        checkRequestBody(request)
        data        = json.loads(request.body)
        
        # '좋아요' 대상 post, comment 와 사용자정보
        if not 'content_id' in data or not 'account' in data:
            return JsonResponse({"message":"[content_id or [account] is empty."}, status=400)

        content_id = data['content_id']
        account    = data['account']
        user_id    = getUserID(account)
        
        if not Users.objects.filter(id=user_id).exists():
            return JsonResponse({"message":"Can't find user."}, status=400)
            
        if not Contents.objects.filter(id=content_id).exists():
            return JsonResponse({"message":"Can't find target."}, status=400)

        if Likes.objects.filter(user_id=user_id, content_id=content_id).exists():
            pass
        else:
            Likes.objects.create(
                    user_id    = user_id,
                    content_id = content_id
                    )

        return JsonResponse({"message":"SUCCESS"}, status=201)
