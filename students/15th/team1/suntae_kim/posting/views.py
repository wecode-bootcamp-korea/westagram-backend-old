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
            posting_username_id = User.objects.get(username=request.user.username)
            posting_text        = data['posting_text']
            posting_image       = data['posting_image']


            print('posting_request.user:', request.user.username)
            BoardPosting.objects.create(
                posting_image = posting_image,
                posting_text  = posting_text,
                posting_username = posting_username_id
            )
            return JsonResponse({ 'MESSAGE': 'SUCCESS'})
        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'})

    def get(self, request):
        postings = BoardPosting.objects.all()
        results = []
        for posting in postings:
            results.append(
                {
                    "posting_username_id": posting.posting_image,
                    "posting_text"       : posting.posting_text,
                    "posting_image"      : posting.posting_image,
                    "posting_time"       : posting.posting_time
                }
            )

        return JsonResponse({'result' : results }, status=200)

class Comment(View):
    @LoginAuthorization
    def post(self, request):
        data = json.loads(request.body)
        try:
            comment_username = data['comment_username']
            comment_text     = data['comment_text']
            posting_id       = data['posting_id']

            BoardComment.objects.create(
                comment_username = comment_username,
                comment_text     = comment_text,
                posting       = BoardPosting.objects.get(id=posting_id)
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'})
        except:
            return JsonResponse({'MESSAGE' : 'KER_ERROR'})

    def get(self, request):
        comments = BoardComment.objects.all()
        results = []
        for comment in comments:
            results.append(
                {
                    "comment_username" : comment.comment_username,
                    "comment_text" : comment.comment_text,
                    "comment_time" : comment.comment_itme,
                    "posting_id" : comment.posting_id
                }
            )
        return JsonResponse({'RESULT' : results}, status=200)


