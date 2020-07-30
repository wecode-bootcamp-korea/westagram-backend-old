import json

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from user.utils   import LoginConfirm
from .models      import (
    Article,
    Comment,
    Like
)

class ArticleView(View):
    @LoginConfirm
    def post(self, request):
        try:
            data = json.loads(request.body)
            Article(
                head  = data['head'],
                body  = data['body'],
                user = User.objects.get(email = request.user.email)
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'messgae' : 'INVLID_INPUT'}, status=400)

class CommentView(View):
    @LoginConfirm
    def post(self, request):
        try:
            data = json.loads(request.body)
            if Article.objects.filter(head = data['head']).exists():
                Comment(
                    content = data['content'],
                    article = Article.objects.get(head = data['head']),
                    user    = User.objects.get(email = request.user.email)
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_INFORMATION'}, status = 401)
        except KeyError:
            return JsonResponse({'message':'INVLID_INPUT'}, status = 400)

class LikeView(View):
    @LoginConfirm
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = User.objects.filter(email = request.user.email)
            if user[0] and Article.objects.filter(head = data['head']).exists():
                article = Article.objects.filter(head = data['head'])
                if Like.objects.filter(user = user[0]).exists():
                    like_user = Like.objects.get(user = user[0].id)
                    if like_user.article == article[0]:
                        like_user.delete()
                        return JsonResponse({'message': 'UNLIKE'}, status=200)
                    else:
                        like_user.article = article[0]
                        return JsonResponse({'message': 'LIKE'}, status=200)
                else:
                    Like(
                        user = user[0],
                        article = article[0]
                    ).save()
                    return JsonResponse({'message': 'LIKE'}, status=200)
            else:
                return JsonResponse({'message': 'NOT_EXISTS'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'INVALID_INPUT'}, status=400)
