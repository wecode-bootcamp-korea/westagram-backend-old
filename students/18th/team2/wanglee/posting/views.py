import json
from django.views    import View
from django.http     import JsonResponse
from .models         import Post
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
                'user' :post.user.username,
                'time' :post.time,
                'head' :post.head,
                'body' :post.body,
                'image':post.image
            }
            results.append(result)
        return JsonResponse({'result': results}, status=200)