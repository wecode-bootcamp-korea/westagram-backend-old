import json

from django.http  import JsonResponse
from django.views import View

from user.models import User
from .models     import Posting


class PostFeedView(View):
    def post(self, request):
        data    = json.loads(request.body)
        user    = data['user']
        image   = data['image']
        content = data['content']
        
        user = User.objects.get(username = user)
        Posting.objects.create(user=user, image=image, content=content)
        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def get(self, request):

        postings = Posting.objects.all()

        result = []
        for posting in postings:
            post_feed = {
                'user'   : posting.user.username,
                'image'  : posting.image,
                'content': posting.content
            }
            result.append(post_feed)

        return JsonResponse({'result': result}, status = 200)
    


