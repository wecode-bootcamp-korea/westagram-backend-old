import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Post, Comment
from users.models       import Account
from utils              import login_decorator


class PostingView(View):
    @login_decorator
    def get(self, request):
        postings = Post.objects.all()
        result = []

        result = [
                {
                    'account'   : postings[i].account.nickname,
                    'image_url' : postings[i].image_url,
                    'contents'  : postings[i].contents,
                    'create_at' : postings[i].create_at,
                }
        for i in range(len(postings))] 
        return JsonResponse({'message' : 'SUCCESS'}, status=200)



    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try :
            account = Account.objects.get(nickname=data['nickname'])

            Post.objects.create(
                account   = account,
                image_url = data['image_url'],
                contents  = data['contents'],
                
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class CommentView(View):
    @login_decorator
    def get(self, request):
        comments = Comment.objects.all()
        result = []

        result = [
                {
                    'account'   : comments[i].account.nickname,
                    'comments'  : comments[i].comments,
                    'create_at' : comments[i].create_at,
                }
        for i in range(len(comments))]
        return JsonResponse({'message' : 'SUCCESS'}, status=200)


    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try :
            account = Account.objects.get(nickname=data['nickname'])
            posting = Post.objects.get(contents=data['contents'])

            Comment.objects.create(
                account  = account,
                comments = data['comments'],
                posting  = posting,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
