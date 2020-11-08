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
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem

        data = json.loads(request.body)

        # image_url, user account 정보를 추출하여 posts table에 추가 작업
        keys        = ['account', 'image_url', 'article'] 
        inputs      = {k:v for k,v in data.items() if k in keys}
        
        for key in keys:
            if not key in inputs:
                return JsonResponse({"message":"we need to take all values [account, image_url, article]"},
                        status=400)
        
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
            posts.append({"article":row.content.article, "image_url":row.image_url, 
                            "created_at":row.content.created_at , "user":row.content.user.name})
        
        return JsonResponse({"posts":posts}, status=200)

class AddComment(View):
    def post(self, request):
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
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
            return JsonResponse({"message":"content_id is empty."}, status=400) 

        user_id     = getUserID(inputs[ACCOUNT])
        
        if user_id == None:
            return JsonResponse({"message":"Can't find user."}, status=400)

        if Contents.objects.filter(id=inputs[CONTENT_ID]).exists():
            inputs['parent_content_id'] = inputs[CONTENT_ID]
        else:
            return JsonResponse({"message":"can't find target content."}, status=401)
        
        Contents.objects.create(
                        article     = inputs[ARTICLE], 
                        created_at  = datetime.now(), 
                        user_id     = user_id
                        )
        
        Comments.objects.create(
                            content_id          = Contents.objects.last().id,
                            parent_content_id   = inputs["parent_content_id"],
                            )

        return JsonResponse({"message":"SUCCESS"}, status=201)
            

class ShowAllComments(View):
    def get(self, request):
        entries     = Comments.objects.select_related('content').select_related('content__user') \
                        .all()
        comments    = []
        for row in entries:
            comments.append({'article':row.content.article, 'created_at':row.content.created_at,
                            'user':row.content.user.name})
        
        return JsonResponse({"comments":comments}, status=200)

class ShowCommentsOfContent(View):
    def post(self, request):
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
        
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
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
        
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

class RemoveContent(View):
    def post(self, request):
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
        
        data    = json.loads(request.body)

        if not 'content_id' in data:
            return JsonResponse({"messge":"[content_id] is empty."}, status=400)

        entries = Contents.objects.filter(id=data['content_id'])

        for row in entries:
            row.delete()
            
        return JsonResponse({"messge":"SUCCESS"}, status=201)


class UpdatePost(View):
    def post(self, request):
        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
        
        data    = json.loads(request.body)

        if not 'content_id' in data:
            return JsonResponse({"messge":"[content_id] is empty."}, status=400)

        if not 'article' in data:
            return JsonResponse({"messge":"[article] must not be empty."}, status=400)

        if not 'image_url' in data:
            return JsonResponse({"messge":"[image_url] must not be empty."}, status=400)

        targets = Posts.objects.filter(content_id=data['content_id'])
        targets.update(image_url=data['image_url'])

        targets = Contents.objects.filter(id=data['content_id'])
        targets.update(
                article     = data['article'], 
                created_at  = datetime.now()
                )
                
        return JsonResponse({"messge":"SUCCESS"}, status=201)



class GetMyPosts(View):    
    def post(self, request):
        def findChildCommentsRecursive(self, parent_content_id):
            rows    = Comments.objects.select_related('content').select_related('content__user') \
                    .filter(parent_content_id = parent_content_id)
            
            childs  = []

            for row in rows:
                data = {
                    "content_id" : row.content_id,
                    "name"       : row.content.user.name,
                    "article"    : row.content.article,
                    "created_at" : row.content.created_at,
                    "comments"   : []
                     }

                data['comments'] = findChildCommentsRecursive(self, row.content_id)
                childs.append(data)

            return childs
 

        has_problem = checkRequestBody(request)
        if has_problem:
            return has_problem
        
        data        = json.loads(request.body)

        # 내가 만든 Post 및 해당 post 에 달린 댓글과 좋아요 정보 모두 제공하기.
        if not 'account' in data:
            return JsonResponse({"message":"Can't receive [account] info"}, status=400)
        
        # 1. request 정보 중 'account'를 통해 user id 추출시도한다. 없으면 안내문구  리턴
        user_id = getUserID(data['account'])
        if user_id == None:
            return JsonResponse({"message":"Can't find user."}, status=400)

        # 2. 해당 user의 contents 정보를 검색, Post에 해당하는 content 없으면 안내문구 리턴
        if not Contents.objects.select_related('user').filter(user_id=user_id).exists():
            return JsonResponse({"message":"User's post is not exist."}, status=400)

        contents    = Contents.objects.select_related('user').filter(user_id=user_id)
        result      = []

        # 3. Contents rows 중 user id에 매칭되는 contents 만 추출하여 looping
        for content in contents:

            # 4. post에 해당하는 content 추출.
            posts       = Posts.objects.select_related('content').select_related('content__user') \
                            .filter(content_id=content.id)
            
            if len(posts) == 0:
                continue

            post_info   = {}
            
            # 5. User가 작성한 post가 있다면 관련 정보를 dictionary로 저장
            for post in posts:
                post_info['content_id'] = content.id
                post_info['image_url']  = post.image_url
                post_info['article']    = post.content.article
                post_info['created_at'] = post.content.created_at
                post_info['user']       = post.content.user.name

                # 6. post를 기준으로 댓글 tree 정보를 재귀호출방식으로 추출.
                post_info['comments']   = findChildCommentsRecursive(self, content.id)
                
                result.append(post_info)

        if len(result) == 0:
            return JsonResponse({"message":"User's post is not exist."}, status=400)
        
        return JsonResponse({"result":result}, status=201)

