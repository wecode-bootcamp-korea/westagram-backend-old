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
            user         = User.objects.get(username=username)

            if username != Users.objects.get(username=username):
                return JsonResponse({"message" : "INVALID_USER"})

            Posting.objects.create(
                username     = user.id,
                description  = description,
                image_url    = image_url
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
                
# get한 사람이 post한 사람과 맞는지 확인 -> 유저와 유저 아이디가 맞는지 확인해야함
# 여러개의 포스팅이 들어올 수 있다


