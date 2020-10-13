import json
from django.http     import JsonResponse 
from django.views    import View  
from user.models     import User
from posting.models  import Post, Image_urls, Comment

class PostView(View):
    
    def post(self, request) :
        data = json.loads(request.body)
        user_id = User.objects.get(user_name=data['user_name'])
        post_id = Post.objects.create(
                contents = data['contents'],
                user = user_id
        )
        for image_url in data['image_url'] :
            Image_urls.objects.create(
                    image_url = image_url,
                    post = post_id
            )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
    
    def get(self, request) :
        post_all = Post.objects.values('id','contents','time','user__user_name')
        post_list   = []
        for post in post_all :
            image_urls = Image_urls.objects.filter(post=post['id'])
            post['image_url'] =[]
            for image in image_urls :
                post['image_url'].append(image.image_url)
            post_list.append(post)
        return JsonResponse({'post_all' :post_list}, status=201) 

class CommentView(View) :

    def post(self, request) :
        data      = json.loads(request.body)
        post      = data['post_id']
        contents  = data['contents']
        user_name = data['user_name']

        user_id = User.objects.get( user_name = user_name )
        post_id = Post.objects.get( id = post)
        Comment.objects.create(user=user_id, post=post_id, contents=contents)
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    def get(self, request, post_id) :
        comments = Comment.objects.filter(post = post_id).values('user__user_name', 'contents', 'time')
        return JsonResponse({'MESSAGE': list(comments) }, status=201)

