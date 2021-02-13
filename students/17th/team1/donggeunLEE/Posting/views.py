import json

from django.http   import HttpResponse, JsonResponse
from django.views  import View
from django.utils  import timezone

from User.models   import Userinfo
from .models       import UserPosting, UserComment, Userlike, AdditonalComment
from User.utilities import login_decorator


# Mission4
# 게시물 작성 및 기능 담당
class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            user      = request.user
            image_url = data['image_url']
            
            UserPosting.objects.create(
                    user_ID   = user,
                    image_url = image_url
                    )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)

    def get(self, request):
        post_list = [{
            'user'      : UserPosting.user_ID.name,
            'image_url' : UserPosting.image_url,
            'create_at' : UserPosting.create_at,
            } for post in UserPosting.objects.all()
            ]
        return JsonResponse({'data': post_list}, status=200)

# 다른 기능들  post_id를 받아서 처리할 수 있는 기능을 모아둔 곳
class PostDetailView(View):
    @login_decorator
    def delete(self, request, post_id):
        data = json.loads(request.body)
        
        try :
            # post_id가 있는지 확인
            if not UserPosting.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE" : "INVALID_POST"}, status=400)

            post = UserPosting.objects.get(id = post_id)

            # 삭제를 요청한 id와 post를 한 id가 같은지를 확인
            if post.user_id != request.user:
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=401)

            # 그냥 삭제 후 성공했다는 코드 송신
            post.delete()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        
        
        # 내가짠 코드
        #if UserPosting.objects.filter(id = user_id, image_url = image_url).exists():
            #UserPosting.objects.get(id=user_id, image_url=image_url).delete()
            #return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
    
    # Mission9 게시물 수정
    # update
    @login_decorator
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            
            # post가 존재하는지 확인
            if not UserPosting.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE" : "INVALID_POST"}, status=400)
            
            post = UserPosting.objects.get(id=post_id)

            if post.user_id != request.user_id:
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)

            # get을 사용해서 default값을 줌으로써 바뀌면 변경 아니면 default값
            post.image_url = data.get('image_url', post.image_url)
            post.create_at = timezone.datetime.now()
            post.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_REQUEST"}, status=400)

    @login_decorator
    def get(self, request):
        user   = request.user
        result = []
        posts  = UserPosting.objects.all()

        for post in posts:
            result.append(
                    {   
                        'user_ID'     : dict(user),
                        'image_url'   : UserPosting.image_url,
                        'posted_time' : UserPosting.create_at
                        }
                    )
        return JsonResponse({"MESSAGE": "SUCCESS", "result" : result}, status=200)
       

    @login_decorator
    def get(self, request, post_id):
        if not UserPosting.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE" : "INVALID_POST"}, status=400)


    


# Mission5
class CommentView(View):
    @login_decorator
    def post(self, request):
        try:    
            data    = json.loads(request.body)
            user    = request.user
            post_id = data.get('post', None)
            comment = data.get('comment', None)

                
            if UserPosting.objects.filter(id=post_id).exists():

                UserComment.objects.create(
                        user_id = user,
                        image   = post_id,
                        comment = comment
                        )
                return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
            return JsonResponse({"MESSAGE":"INVALID_IMAGE"}, status=400)
        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
    

# Misson8 댓글 제거
class CommentDetailView(View):
    @login_decorator
    def delete(self, request, comment_id):
        try:
            data = json.loads(request.body)

            if not UserComment.objects.filter(id=comment_id).exists():
                return JsonResponse({"MESSAGE" : "INVALID_COMMENT"}, status=400)

            comment = UserComment.objects.get(id=comment_id)

            if comment.user != request.user:
                return JsonResponse({"MESSAGE" : "INVALID_USER"})

            comment.delete()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)

            #if UserComment.objects.filter(comment = data['comment']).exists():
                #UserComment.objects.get(comment=data['comment']).delete()
                #return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

    # update
    @login_decorator
    def post(self, request, comment_id):
        try:
            # 새로 받은 comment
            data = json.loads(request.body)
            new_comment = data.get('comment', None)

            comment = UserComment.objects.get(id=comment_id)

            if comment.user_id != request.user:
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=400)

            comment.comment = new_comment
            comment.save()
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)


class AddCommentView(View):
    @login_decorator
    def post(self, request, comment_id):
        data       = json.loads(request.body)
        user       = request.user
        user_id    = user.id
        comment_id = UserComment.objects.get(id = comment_id)

        AdditonalComment.objects.create(
                comment    = comment_id,
                name       = user.name,
                addcomment = data['addcomment']
                )
        return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        

#Mission6 좋아용 구현하기
class LikeView(View):
    @login_decorator
    def post(self, request):
        # 좋아요가 있으면 제거, 없으면 post
        try:
            data  = json.loads(request.body)
            user  = request.user
            image = data.get(data['image'], None)

            if not UserPosting.objects.filter(image_url = post):
                return JsonResponse({"MESSAGE" : "INVALID_POST"}, status=400)

            post = UserPosting.objects.get(image_url = image)

            if Userlike.objects.filter(post = post.id, user=user).exists():
                Userlike.objects.get(post=post.id, user=user).delete()
                return JsonResponse({"MESSAGE" : "DELETE_SUCCESS"}, status=200)
            
            Userlike.objects.create(
                    post = post.id,
                    user = user
                    )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)


