import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Post, Comment, Like, Follow
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
    
    @login_decorator
    def delete(self, request):

        try:
            data    = json.loads(request.body)
            account = request.account

            contents_id = data['contents_id']

            if Post.objects.filter(id=contents_id).exists():
                Post.objects.get(id=contents_id).delete()
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'POST_DOES_NOT_EXIST'},status=401)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    @login_decorator
    def patch(self, request):

        try:
            data    = json.loads(request.body)
            account = request.account

            contents    = data['contents']
            image_url   = data['image_url']
            contents_id = data['contents_id']
            post        = Post.objects.get(id=contents_id)


            if post.account.id == account.id:
                if image_url:
                    post.image_url = image_url
                if contents:
                    post.contents  = contents
                post.save()
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'NOT_WRRITER'}, status=400)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
            

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
            account    = Account.objects.get(nickname=data['nickname'])
            posting    = Post.objects.get(contents=data['contents'])

            if 'comments_id' in data:
                Comment.objects.create(
                        account     = account,
                        comments    = data['comments'],
                        posting     = posting,
                        comments_id = data['comments_id'],
                        level       = 2
                )
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)

            Comment.objects.create(
                account  = account,
                comments = data['comments'],
                posting  = posting,
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request):
        data = json.loads(request.body)

        try :
            data    = json.loads(request.body)
            account = request.account

            comments_id = data['comments_id']

            if Comment.objects.filter(id=comments_id).exists():
                Comment.objects.get(id=comments_id).delete()
                return JsonResponse({'message' : 'SUCCESS'}, status=200)

            return JsonResponse({'message':'POST_DOES_NOT_EXIST'},status=401)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class LikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try :
            print(request.account)
            account = Account.objects.get(nickname=data['nickname'])
            posting = Post.objects.get(contents=data['contents'])

            if not account or not posting:
                return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

            if Like.objects.filter(posting=posting, account=account).exists():
                Like.objects.filter(posting=posting, account=account).delete()
                return JsonResponse({'message' : 'DELETE_LIKE'}, status = 200)

            Like.objects.create(
                account = account,
                posting = posting
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)


class FollowView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try :
            follower  = request.account
            following = Account.objects.get(nickname=data['following'])

            if not follower or not following:
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

            if Follow.objects.filter(follower=follower, following=following).exists():
                Follow.objects.filter(follower=follower, following=following).delete()
                return JsonResponse({'message' : 'DELETE_FOLLOWING'}, status=200)

            Follow.objects.create(
                follower  = follower,
                following = following
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
