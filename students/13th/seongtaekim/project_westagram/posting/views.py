import json
from django.http     import JsonResponse 
from django.views    import View  
from user.models     import User
from posting.models  import Post, Image_urls

class PostView(View):
    
    def post(self, request) :
        data = json.loads(request.body)
        user_id = User.objects.get(user_name=data['user_name'])
        post_id = Post.objects.create(
                content = data['content'],
                user = user_id
        )
        for image_url in data['image_url'] :
            Image_urls.objects.create(
                    image_url = image_url,
                    post = post_id
            )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
    
    def get(self, request) :
        post_all = Post.objects.values('id','content','time','user__user_name')
        post_list   = []
        for post in post_all :
            image_urls = Image_urls.objects.filter(post=post['id'])
            post['image_url'] =[]
            for image in image_urls :
                post['image_url'].append(image.image_url)
            post_list.append(post)
        return JsonResponse({'post_all' :post_list}, status=201) 
