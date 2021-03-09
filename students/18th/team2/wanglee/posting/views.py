import json
from django.views    import View
from django.http     import JsonResponse
from .models         import Post, Reply, Like
from account.models  import User

class PostManage(View):
    def post(self, request):
        data      = json.loads(request.body)
        userinfo  = data.get('user')
        head      = data.get('head')
        body      = data.get('body')
        image     = data.get('image')
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
                'image':post.image,
                'likes':post.like_count
            }
            results.append(result)
        return JsonResponse({'result': results}, status=200)

class ReplyManage(View):
    def post(self, request):
        data     = json.loads(request.body)
        postinfo = data.get('post')
        userinfo = data.get('user')
        body     = data.get('body')
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

class LikeManage(View):
    def post(self, request):
        data     = json.loads(request.body)
        postinfo = data.get('post')
        userinfo = data.get('user')
        post     = Post.objects.get(pk=postinfo)
        user     = User.objects.get(username=userinfo)
        likeds   = Like.objects.filter(post=post, user=user)

        for liked in likeds:
            count = Post.objects.get(pk=postinfo).like_count
            Post.objects.filter(pk=postinfo).update(like_count=count-1)
            Like.objects.get(post=post, user=user).delete()
            return JsonResponse({'result': "unliked"}, status=200)

        count = Post.objects.get(pk=postinfo).like_count
        Post.objects.filter(pk=postinfo).update(like_count=count+1)
        Like.objects.create(post=post, user=user)
        return JsonResponse({'result': "liked"}, status=200)