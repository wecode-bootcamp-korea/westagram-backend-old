import json

from django.views import View
from django.http  import JsonResponse

from .models        import Posting, Comment, Like
from account.models import User

class PostingView(View):
    def post(self, request):
        #딕셔너리 모양으로 받아들여진 정보(httpie에 입력한 정보)
        data    = json.loads(request.body)
        user    = User.objects.get(email=data['email'])
        posting = Posting.objects.create(
            img_url = data["img_url"],
            user    = user
            #Time은 알아서 import, 입력 필요 없음.
        )
        return JsonResponse({"message" : "SUCCESS"}, status=200)

class ShowView(View):    
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
            
        return JsonResponse({"result" : result}, status=200)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        img_url = Posting.objects.get(img_url=data['img_url'])
        user    = User.objects.get(email=data['email'])
        comment = Comment.objects.create(
            comment = data["comment"],
            img_url = img_url,
            user    = user
        )
        return JsonResponse({"message":"SUCCESS"}, status=200)
    
class CommentShowView(View):
    def get(self, request):
        commentshows = Comment.objects.filter(img_url=1)
        # id 값이 1번인 게시글의 등록된 댓글들만(그래서 filter, get아님) 출력
        result = []
        
        for commentshow in commentshows:
            my_dict = {
                'user'    : commentshow.user.email,
                'comment' : commentshow.comment,
            }
            result.append(my_dict)
        
        return JsonResponse({"result" : result}, status=200)