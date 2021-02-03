import json
import my_settings
import datetime

from django.views      import View
from django.http       import JsonResponse

from user.models    import User
from posting.models import Posting, Comment

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

class CommentsView(View):
    def get(self, request, posting_id):
        comments = Posting.objects.filter(posting_id=posting_id)
        result  = []

        for comment in comments:
            result.append(
                {
                    'nickname'    : comments.user.nickname,
                    'text'        : comments.text,
                    'posted_time' : comments.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    def post(self, request, posting_id):
        try:
            data = json.loads(request.body)
            
            text     = data['text']
            nickname = data['nickname']

            if User.objects.filter(nickname=nickname).exists():
                Comment.objects.create(
                    text     = text,
                    posting  = Posting.objects.get(id=posting_id),
                    user     = User.objects.filter(nickname=nickname)[0]
                )
                return JsonResponse({'message':'SUCCESS'},status=200)
            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)