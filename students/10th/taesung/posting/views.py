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
            if User.objects.filter(name = data['name']).exists() and not Article.objects.filter(head = data['head']).exists():
                Article(
                    user = User.objects.get(name= data['name']),
                    head = data['head'],
                    body = data['body']
                ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'messgae' : 'FAIL'}, status=400)


class Comment(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(name=data['name']).exists() and Article.objects.filter(head = data['head']).exists():
                Comment(
                    content = data['content'],
                    name    = User.objects.get(name = data['name']),
                    article = Article.objects.get(head = data['head'])
                ).save()
                return JsonResponse({'message': 'SUCCESS'}, status=200)
        except:
            return JsonResponse({'message':'ERROR'}, status = 400)
