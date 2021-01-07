import json
import re

from django.http  import JsonResponse
from django.views import View

from user.utils      import login_required
from user.models     import User
from posting.models  import Article


class PostingView(View):

    @login_required
    def post(self, request):
        
        try:
            data       = json.loads(request.body)
            user_id    = request.user_id
            content    = data["content"]
            image_urls = data["image_urls"] # list

            for image_url in image_urls:
                created_article = Article.objects.create(
                        user      = User.objects.get(id=user_id),
                        content   = content,
                        image_url = image_url
                        )
            
            return JsonResponse({'MESSAGE': 'POSTED'}, status=200)
        
        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)


class GetArticlesView(View):
    
    def get(self, request):
        try:
            message = {}
            
            for article in Article.objects.all():
                message[article.id] = {
                        "created_user" : User.objects.get(id=article.user_id).username,
                        "image_url"    : article.image_url,
                        "content"      : article.content,
                        "created"      : article.created
                        }

            return JsonResponse(message, status=200)
        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)




