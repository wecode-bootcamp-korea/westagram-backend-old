import json
from json               import JSONDecodeError

from django.http        import JsonResponse, HttpResponse
from django.shortcuts   import get_object_or_404
from django.views       import View
from django.utils       import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models        import PostModel, CommentModel
from Account.models import User

# 게시물 등록 뷰
class UploadPost(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)
            
        # try:
        #     upload_user = data['username']
        #     upload_text = data['text']
        #     upload_img_url = data['url']
        # except KeyError:
        #     return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        #if 문으로 try except 대체할 수 있으면, if문으로 대체 : 부하 훨씬 적음
        chk = 0
        for key in data:
            if key == 'username' or key =='text' or key=='url':
                chk+=1
        if chk < 3:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        upload_user = data['username']
        upload_text = data['text']
        upload_img_url = data['url']

        try:
            user_obj = User.objects.get(username=upload_user)
        except ObjectDoesNotExist: # 게시물을 등록한 유저정보가 데이터베이스에 없음
            return JsonResponse( {"message": "INVALID_USER"}, status=401)

        p = PostModel(
            user = user_obj,
            text = upload_text,
            img_url = upload_img_url,
        )

        p.save()
        return JsonResponse({'message':'POST_SUCCESS'}, status=200)

# 게시물 호출 뷰
class ShowPost(View):
    def get(self, request):
        post_data = PostModel.objects.values()
        return JsonResponse({'post':list(post_data)},status=200)

# 댓글 등록 뷰
class UploadComment(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)


        # try:
        #     comment_user = data['username']
        #     comment_text = data['text']
        #     comment_post_id = data['post_id'] # 댓글이 달리는 게시물 id
        # except KeyError:
        #     return JsonResponse({"message": "KEY_ERROR"}, status=400)

        chk = 0
        for key in data:
            if key == 'username' or key =='text' or key=='post_id':
                chk+=1
        if chk < 3:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
        comment_user = data['username']
        comment_text = data['text']
        comment_post_id = data['post_id']

        try:
            user_info = User.objects.get(username=comment_user)
        except ObjectDoesNotExist: # 게시물을 등록한 유저정보가 데이터베이스에 없음
            return JsonResponse( {"message": "INVALID_USER"}, status=401)

        try:
            post_info = PostModel.objects.get(id=comment_post_id)
        except ObjectDoesNotExist:
            return JsonResponse( {"message": "INVALID_POST"}, status=401)
        
        CommentModel(
            user = user_info,
            post = post_info,
            text = comment_text
        ).save()

        return JsonResponse({'message':'COMMENT_SUCCESS'}, status=200)
    
# 댓글 표출 뷰
class ShowComment(View):
    def get(self, request):
        post_id = request.GET.get('post_id') 
        if not post_id : # query parameter가 없으면 
            comment_list = list(CommentModel.objects.values()) # 모든 댓글표출
            return JsonResponse({'comments':comment_list},status=200)
        else: # [추가 구현 사항] : 댓글은 특정 게시물을 기준으로 분류. 1번 게시물에 등록된 댓글만을 표출할 수 있도록 구현
            comment_list = list(CommentModel.objects.filter(post=post_id).values())
            if not comment_list:
                return JsonResponse({'message':'NO_COMMENT'}, status=200)
            else:
                return JsonResponse({'comments':comment_list},status=200)
            
        

    