import json

from django.http    import JsonResponse
from django.views   import View

from user.utils     import login_decorator
from user.models    import Account
from .models        import Post, Comment


class PostingView(View):
    @login_decorator
    def post(self,request):
        print(request.body) # 바이트화되서 프린트됨
        data = json.loads(request.body)
        print(data) #스트링으로 프린트댐
        user = Account.objects.get(id=request.user.id)

        Post(
            author = user, # 객체를 담음 (엄밀하게는 user_id가 담김)
            content = data['content'],
            image_url = data['image_url']
        ).save()
        
        return JsonResponse({'MESSAGE':'POST_CREATED!'}, status = 201)

class ReadPostingView(View):
    @login_decorator
    def get(self,request):
        #data = json.loads(request.body)
        posts = Post.objects.all()

        if not posts:
            return JsonResponse({'MESSAGE':'POST_NOT_FOUND'}, status = 404)

        postings = [{
            'post_id' : post.id,
            'post_author' : post.author.id,
            'post_content' : post.content,
            'post_image_url' : post.image_url,
            'post_created' : post.created_at}        for post in posts]
        return JsonResponse({'posts':postings}, status = 200)

class CreateCommentingView(View):
    @login_decorator
    def post(self,request):
        data = json.loads(request.body)
        user = Account.objects.get(id=request.user.id)

        comment = data['comment']

        if not Post.objects.filter(id = data['post_id']).exists():
            return JsonResponse ({'MESSAGE':'POST_NOT_FOUND'}, status = 404)
        if len(comment) > 300:
            return JsonResponse ({'MESSAGE':'TOO_MUCH_TALK'}, status = 400)
            
        Comment(
            author = user,
            comment = data['comment'],
            post_id = data['post_id']
        ).save()
        return JsonResponse({'MESSAGE':'COMMENT_CREATED!'})

class ReadCommentingView(View):
    @login_decorator
    def get(self, request):
        data = json.loads(request.body)
        try:
            comments = Comment.objects.filter(post_id = data['post_id'])

            if not comments.exists():
                return JsonResponse({'MESSAGE':'NO_COMMENT_EXIST!'}, status = 400)

            comments = [{
                'author' : comment.author.id,
                'comment' : comment.comment} for comment in comments]
            return JsonResponse({'comments': comments}, status = 200)
        except KeyError:
            JsonResponse({"message":"KEY_ERROR"}, status = 400)

