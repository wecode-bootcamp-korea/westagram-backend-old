from django.views import View
from django.http import JsonResponse
import json
from .models import Posting
from user.models import User
import datetime


class PostingView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)
            user = User.objects.get(user_name=data["user"])
            if not User.objects.filter(pk=user.pk).exists():

                return JsonResponse({"message": "This user does not exist!"})

            Posting.objects.create(
                image_url=data["image_url"], content=data.get("content"), user=user
            )

            return JsonResponse({"message": "Posting SUCCESS!"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KeyError!"}, status=400)

        except Exception as ex:
            return JsonResponse({"Error occurred": f"{ex}"}, status=400)

    def get(self, request):
        posts = Posting.objects.all()
        post_list = []
        for post in posts:

            post_data = {
                "image_url":  post.image_url,
                "content":    post.content,
                "created_at": str(post.created_at),
                "updated_at": str(post.updated_at),
                "user":       post.user,
            }
            post_list.append(post_data)
        return JsonResponse({"message": "posting get success"}, status=200)
