import json
import re

from django.views        import View
from django.http         import JsonResponse

from user.models    import Account
from models         import Post

class PostingView(View):
    @auth_decorator
    def post(self,request):
        data = json.loads(request.body)
        
        Post(
            user        = Account.objects.get(id=data['user']),
            content     = data['content'],
            image_url   = data['image_url'] #생성시간은 자동으로 추가
        ).save()
        return JsonResponse({'MESSAGE':'CREATED'}, status=201)
    
    def get(self,request):
        data = json.loads(request.body)


#작업중