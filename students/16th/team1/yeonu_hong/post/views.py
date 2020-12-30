import json
from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from .models          import Post, Image
from user.models      import User
from datetime         import datetime

# Create your views here.
class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if not User.objects.filter(name=data['user']):
                return JsonResponse({'message':'INVALID_USER'}, status=400)
            
            user     = User.objects.get(name=data['user'])
            image    = data['image']
            pub_date = datetime.now() # 2020-12-30 11:47:45.781887

            Post.objects.create(user=user, pub_date=pub_date)
            post = Post.objects.filter(user=user).last() # 한 유저가 여러개의 포스트 작성 가능. 지금 들어온 포스트로 가져와야함
            Image.objects.create(post=post,image=image)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)



    

