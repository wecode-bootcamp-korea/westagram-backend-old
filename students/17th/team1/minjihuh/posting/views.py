import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models      import (
    User
)
from posting.models    import (
    Posting
)

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            image_url    = data['image_url']
            description  = data.get('description', None) #null=True
            username     = data['username']

            if not username: 
                return JsonResponse({"message" : "INVALID_USER"}, status=400)
            
            if not image_url:
                return JsonResponse({"message": "REQUIRED_IMAGE_FIELD"}, status=400)

            if User.objects.filter(username=username).exists():
                Posting.objects.create(
                username=username,
                image_url=image_url,
                description=description
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}) 
                
# get한 사람이 post한 사람과 맞는지 확인 -> 유저와 유저 아이디가 맞는지 확인해야함
# 여러개의 포스팅이 들어올 수 있다


