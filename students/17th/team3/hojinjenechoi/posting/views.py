import json
import my_settings
import datetime

from django.views      import View
from django.http       import JsonResponse

from user.models    import User
from posting.models import Posting

class PostingView(View):
    def get(self, request):
        postings = Posting.objects.all()
        result  = []

        for posting in postings:
            result.append(
                {
                    'nickname'    : posting.user.nickname,
                    'image'       : posting.image,
                    'caption'     : posting.caption,
                    'posted_time' : posting.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    def post(self, request):
        try: 
            data = json.loads(request.body)

            image    = data['image']
            caption  = data.get('caption', None)
            nickname = data['nickname']

            if User.objects.filter(nickname=nickname).exists():
                Posting.objects.create(
                    image    = image,
                    caption  = caption,
                    user     = User.objects.filter(nickname=nickname)[0]
                )
                return JsonResponse({'message':'SUCCESS'},status=200)
            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    

# http -v POST 127.0.0.1:8000/posting/post image='http://image.dongascience.com/Photo/2020/03/5bddba7b6574b95d37b6079c199d7101.jpg' caption='Cute Doggo' nickname='youjin'

