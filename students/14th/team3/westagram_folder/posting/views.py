import json

from django.http    import JsonResponse
from django.views   import View

from user.utils     import login_decorator
from user.models    import Account
from .models        import Post


class PostingView(View):
    @login_decorator
    def post(self,request):
        print(request.body)
        data = json.loads(request.body)
        print(data)
        user = Account.objects.get(id=request.user.id)

        Post(
            author = user, # 객체를 담음 (엄밀하게는 user_id가 담김)
            content = data['content'],
            image_url = data['image_url']
        ).save()
        
        return JsonResponse({'MESSAGE':'CREATED'}, status = 201)

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