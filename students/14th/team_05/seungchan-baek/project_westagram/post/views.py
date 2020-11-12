import json

from django.views import View
from django.http  import JsonResponse, request

from .models      import Posting, Comment
from user.models  import User
from user.utils   import login_decorator

# 게시판 등록
class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id = data['user_id'])

        try:
            Posting.objects.create(description = data['description'] ,content = data['content'] ,author=user)
        
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
# 게시판 읽기        
    def get(self,request):
        posts  = Posting.objects.all()
        result = []
        
        for post in posts:
            read_posting ={
                'author'      :   post.author.name,
                'content'     :   post.content,
                'description' :   post.description,
                'postedTime'  :   str(post.postedtime)
            }
            result.append(read_posting)

        return JsonResponse({'result': result})
# 댓글 등록
class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id = data['user_id'])
        post = Posting.objects.get(id = data['post_id'])

        try:
            Comment.objects.create(content = data['content'], user = user, post=post)
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
# 댓글 읽기
    def get(self, request):
        data = json.loads(request.body)
        result = []
        comments= Comment.objects.filter(post= data['user_id'])
        
        for comment in comments:
            read_comments = {
                'content'    :   comment.content,
                'postedtime' :   str(comment.postedtime)
            }
            result.append(read_comments)

        return JsonResponse({"message" :result }, status =200)