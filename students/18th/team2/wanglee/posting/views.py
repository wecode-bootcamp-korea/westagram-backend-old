import json
from django.views    import View
from django.http     import JsonResponse
from .models         import Post, Reply
from account.models  import User

class PostManage(View):
    def post(self, request):
        data      = json.loads(request.body)
        userinfo  = data['user']
        head      = data['head']
        body      = data['body']
        image     = data['image']
        user      = User.objects.get(username=userinfo) 

        Post.objects.create(user=user, head = head, body = body,  image=image)
        return JsonResponse({'result': 'SUCCESS'}, status=200)
    
    def get(self, request):
        posts   = Post.objects.all()
        results = []
        for post in posts:
            result = {
                'username' :post.user.username,
                'time' :post.time,
                'head' :post.head,
                'body' :post.body,
                'image':post.image
            }
            results.append(result)
        return JsonResponse({'result': results}, status=200)

class ReplyManage(View):
    def post(self, request):
        data     = json.loads(request.body)
        postinfo = data['post']
        userinfo = data['user']
        body     = data['body']
        post     = Post.objects.get(pk=postinfo)
        user     = User.objects.get(username=userinfo)

        Reply.objects.create(post=post, user=user, body=body)
        return JsonResponse({'result': 'SUCCESS'}, status=200)

    def get(self, request):
        replies = Reply.objects.all()
        results = []
        post  = {}
        for reply in replies:
            temp = {'post head' : reply.post.head}
            if temp not in results:
                post = temp
                results.append(post)
            result = {
                'username' : reply.user.username,
                'time'     : reply.time,
                'reply'    : reply.body,
            }
            results.append(result)
        return JsonResponse({'result': results}, status=200)
