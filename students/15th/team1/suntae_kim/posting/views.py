import json
import jwt
import bcrypt

from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from user.models import User
from user.utils import LoginAuthorization
from posting.models import BoardPosting, BoardComment
from django.utils.timezone import now

# Create your views here.


class Posting(View):
    @LoginAuthorization #먼저 실행됨..
    def post(self, request):
        data = json.loads(request.body)
        try:
            username_id = User.objects.get(id=request.user_id)
            text        = data['text']
            image       = data['image']

            BoardPosting.objects.create(
                image    = image,
                text     = text,
                username = username_id
            )
            return JsonResponse({ 'MESSAGE': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

    def get(self, request):
        postings = BoardPosting.objects.all()
        results = []
        for posting in postings:
            results.append(
                {
                    "username_id": posting.image,
                    "text"       : posting.text,
                    "image"      : posting.image,
                    "time"       : posting.time
                }
            )

        return JsonResponse({'result' : results }, status=200)

class Comment(View):
    @LoginAuthorization
    def post(self, request):
        data = json.loads(request.body)
        try:
            username   = data['username']
            text       = data['text']
            posting_id = data['posting_id']

            BoardComment.objects.create(
                username = username,
                text     = text,
                posting  = BoardPosting.objects.get(id=posting_id)
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        except:
            return JsonResponse({'MESSAGE' : 'KER_ERROR'}, status=400)

    def get(self, request):
        comments = BoardComment.objects.all()
        results = []
        for comment in comments:
            results.append(
                {
                    "username"   : comment.username,
                    "text"       : comment.text,
                    "time"       : comment.itme,
                    "posting_id" : comment.posting_id
                }
            )
        return JsonResponse({'RESULT' : results}, status=200)


