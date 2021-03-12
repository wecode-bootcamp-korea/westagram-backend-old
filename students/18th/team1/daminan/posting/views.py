import json

from django.views import View
from django.http  import JsonResponse

from .models        import Posting, Comment, Like
from account.models import User
from account.views  import TokenCheck

class PostingView(View):
    @TokenCheck    
    def post(self, request):
        #딕셔너리 모양으로 받아들여진 정보(httpie에 입력한 정보)
        data    = json.loads(request.body)
        user    = request.user
        posting = Posting.objects.create(
            img_url = data["img_url"],
            user    = user
            #Time은 알아서 import, 입력 필요 없음.
        )
        return JsonResponse({"message" : "SUCCESS"}, status=200)

class ShowView(View):
    @TokenCheck
    # httpie, postman 기준으로 토큰 안 들어가면 에러남    
    def get(self, request):
        shows  = Posting.objects.all()
        result = []
    
        for show in shows:
            my_dict = {
                'update_time' : show.upload_time,
                'img_url'     : show.img_url,
                'user'        : show.user.email,
            }
            result.append(my_dict)
            # 게시물과 시간, 유저 보기
        return JsonResponse({"result" : result}, status=200)

class CommentView(View):
    @TokenCheck    
    def post(self, request):
        data    = json.loads(request.body)
        img_url = Posting.objects.get(img_url=data['image'])
        user    = request.user
        comment = Comment.objects.create(
            comment = data["comment"],
            image   = img_url,
            # models.py에서 가져와야 하는 것.
            user    = user
        )
        return JsonResponse({"message":"SUCCESS"}, status=200)
    
class CommentShowView(View):
    @TokenCheck    
    def get(self, request):
        commentshows = Comment.objects.filter(image=1)
        # id 값이 1번인 게시글의 등록된 댓글들만(그래서 filter, get아님) 출력
        result = []
        
        for commentshow in commentshows:
            my_dict = {
                'user'    : commentshow.user.email,
                'comment' : commentshow.comment,
            }
            result.append(my_dict)
        
        return JsonResponse({"result" : result}, status=200)
    

class LikeView(View):
    @TokenCheck    
    def post(self,request):
        data  = json.loads(request.body)
        user  = request.user
        img_url = Posting.objects.get(img_url=data['image'])
        like  = Like.objects.create(
        user  = user,
        image = img_url,
    )
        return JsonResponse({"message" : "SUCCESS"}, status=200)