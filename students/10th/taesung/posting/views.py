import json

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from .models      import (
    Article,
    Comment
)

from user.models  import User

class ArticleView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists() and not Article.objects.filter(head = data['head']).exists():
                Article(
                    email = User.objects.get(name= data['email']),
                    head = data['head'],
                    body = data['body']
                ).save()
                return JsonResponse({'message':'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_INFORMATION'}, status=401)
        except KeyError:
            return JsonResponse({'messgae' : 'FAIL'}, status=400)

class CommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists() and Article.objects.filter(head = data['head']).exists():
                Comment(
                    content = data['content'],
                    email   = User.objects.get(name = data['email']),
                    article = Article.objects.get(head = data['head'])
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message': 'INVALID_INFORMATION'}, status = 401)
        except KeyError:
            return JsonResponse({'message':'ERROR'}, status = 400)
