import json

from django.http  import JsonResponse
from django.views import View

from post.models import Post, Comment
from user.models import User
from user.utils  import id_auth


class PostingView(View):
    @id_auth
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            data_writer  = request.user 
            data_img_url = data['img']
            data_content = data['content']

            Post.objects.create(writer = data_writer, img_url = data_img_url, content = data_content)
            return JsonResponse({"message": "SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
    def get(self, request):
        posts    = Post.objects.all()
        user_get = User.objects.get
        results  = []
        for post in posts:
            results.append(
                {
                    "id"      : post.id,
                    "writer"  : user_get(id=post.writer_id).account,
                    "content" : post.content,
                    "datetime": post.datetime,
                    "img"     : post.img_url,
                }
            )
        return JsonResponse({"result": results}, status = 200)


class CommentView(View):
    @id_auth
    def post(self, request):
        data = json.loads(request.body)
        
        data_writer  = request.user
        data_post    = Post.objects.get(id = data['post_id'])
        data_content = data['content']

        Comment.objects.create(post = data_post, writer = data_writer, content = data_content)
        return JsonResponse({"message": "SUCCESS"}, status = 200)

    def get(self, request):
        data     = json.loads(request.body)
        if data['post_id']:
            comments = Comment.objects.filter(post_id = data['post_id'])
        else:
            comments = Comment.objects.all()
        
        results= []
        for comment in comments:
            results.append(
                {
                    "id"      : comment.id,
                    "writer"  : User.objects.get(id = comment.writer_id).account,
                    "content" : comment.content,
                    "datetime": comment.datetime,
                }
            ) 
        return JsonResponse({"results": results}, status = 200)
