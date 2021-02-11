import json

from django.views import View
from django.http  import JsonResponse
from user.models  import User

from . import models

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            post_user = data["user"]
            post_title = data["title"]
            user = User.objects.get(pk=data["user"])
            models.Posting(
                user=user, 
                title=data["title"], 
                content=data["content"],
            ).save()
            return JsonResponse({"message": "SUCESS"},status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=data["user"])
            posting = models.Posting.objects.get(id=data["posting"])
            models.Comment(
                user=user, 
                posting=posting,
                content=data["content"], ).save()
            return JsonResponse({"message": "SUCESS"},status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
class LoveView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=data["user"])
            posting = models.Posting.objects.get(id=data["posting"])
            pk = models.Love.objects.filter(user=user, posting=posting)
            if pk.exists():
                pk.update(is_like=data["is_like"])
                return JsonResponse({"message": "SUCESS UPDATE "},status=200)
            else:
                models.Love(
                    user=user, 
                    posting=posting,
                    is_like=data["is_like"]).save()
                return JsonResponse({"message": "SUCESS CREATE "},status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)