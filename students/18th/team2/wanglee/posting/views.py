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
        posts = Post.objects.all()
        results=[]
        for post in posts:
            result = {
                'user':post.user.username,
                'time':post.time,
                'head':post.head,
                'body':post.body,
                'image':post.image
            }
            results.append(result)
        return JsonResponse({'result': results}, status=200)






        # if email == '' or password == '':
        #     return JsonResponse({"message":"KEY_ERROR"}, status=400)

        # elif '@' not in email or '.' not in email:
        #     return JsonResponse({"message":"email must contain the '@' symbol and the period'.'"}, status=400)
        
        # elif len(password) < 8:
        #     return JsonResponse({"message":"password must be at least 8 characters"}, status=400)
        
        # for temp in temps:
        #     if username == temp.username:
        #         return JsonResponse({"message":"That username is taken. Try another"}, status=400)
        
        #     elif email == temp.email:
        #         return JsonResponse({"message":"That email is taken. Try another"}, status=400)
        
        #     elif phone == temp.phone:
        #         return JsonResponse({"message":"That phone is taken. Try another"}, status=400)

        # User.objects.create(username=username, email=email, password=password, phone=phone)
        # return JsonResponse({'result': 'SUCCESS'}, status=200)
        