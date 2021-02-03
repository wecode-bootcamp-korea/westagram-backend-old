import json

from django.views import View
from django.http  import JsonResponse

from .models     import Posting, Comment, LikePosting
from user.models import Accounts

class PostingView(View):
    def get(self, request):
        postings = Posting.objects.all()

        response_posting = [
            {
                # 'account'  : postings[i].account,
                'account'  : postings[i].account.nickname,
                # 'account'  : 'ㅋㅋㅋ',
                'image_url': postings[i].image_url,
                'contents' : postings[i].contents,
                'create_at': postings[i].create_at,
                'update_at': postings[i].update_at
            }
        for i in range(len(postings))]

        return JsonResponse({'message':'SUCCESS', 'result':response_posting}, status=200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            account = Accounts.objects.get(nickname=data['account'])

            Posting.objects.create(
                account   = account,
                image_url = data['image_url'],
                contents  = data['contents']
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def delete(self, request, account, posting):
        account = Accounts.objects.filter(nickname=account)
        posting = Posting.objects.filter(id=posting)

        try:
            postingExist = Posting.objects.filter(account=account[0], id=posting[0].id)
            if postingExist.exists():
                postingExist.delete()
                return JsonResponse({'message':'SUCCESS'}, status=200)

            return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)
        except IndexError:
            return JsonResponse({'message':'INDEX_ERROR'}, status=400)


class CommentView(View):
    def get(self, request):
        comments = Comment.objects.filter(posting=1)

        comments = [
            {
                'account'   : comment.account.nickname,
                'posting'   : comment.posting.id,
                'contents'  : comment.contents,
                'create_at' : comment.create_at
            } 
        for comment in comments]

        return JsonResponse({'message':'SUCCESS', 'result':comments}, status=200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            account  = Accounts.objects.get(nickname=data['nickname'])
            posting  = Posting.objects.get(id=data['posting'])
            contents = data['contents']

            Comment.objects.create(
                account  = account,
                contents = contents,
                posting  = posting
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def delete(self, request, account, posting, comment):
        account = Accounts.objects.filter(nickname=account)[0]
        
        commentExist = Comment.objects.filter(account=account, posting=posting, id=comment)
        if commentExist.exists():
            commentExist.delete()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        return JsonResponse({'message':'DOES_NOT_EXIST'}, status=400)

class LikePostingView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            account = Accounts.objects.filter(nickname=data['account'])
            posting = Posting.objects.filter(id=data['posting'])
            
            postingExist = LikePosting.objects.filter(account=account[0], posting=posting[0])
            if postingExist.exists():
                postingExist.delete()
                return JsonResponse({'message':'SUCCESS'}, status=400)

            if not account or not posting:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            LikePosting.objects.create(
                account = account[0],
                posting = posting[0]
            )

            return JsonResponse({'message':'SUCCESS'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)