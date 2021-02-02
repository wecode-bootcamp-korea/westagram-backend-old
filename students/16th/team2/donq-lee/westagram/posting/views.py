import json
from django.views   import View
from django.http    import JasonResponse
from posting.models import Post

class PostImgView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        img = data['img']
        content = data['content']
