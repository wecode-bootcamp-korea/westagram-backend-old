import json

from django.views   import View
from django.http    import JsonResponse
from posting.models import Post
from user.models    import User


class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
                
            #user_id = User.objects.get(name=data['name'])
            user_id = data['user_id']
            content = data['content']
            img_url = data['img_url']
       
            if not data['img_url']:
                 return JsonResponse({'MESSAGE':'이미지를 첨부하세요.'},status=400)
            
            else:
                Post.objects.create(
                    #user_id = user_id.id,
                    user_id = user_id,
                    content = content,
                    img_url = img_url
                )
        
            return JsonResponse({'MESSAGE':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KeyError'},status=400)




