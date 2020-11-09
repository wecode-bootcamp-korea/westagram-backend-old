import json
from django.views import View
from django.http import JsonResponse
from posting.models import Posting
from user.models import User


class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            a1 = User.objects.get(id=data["id"])
            Posting.objects.create(user=a1, image_url=data["image_url"])

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        # except Exception:
        #     return JsonResponse({'message': 'INVALID_USER'}, status=401)


    def get(self, request):


        return JsonResponse({"Hello":"Good"}, status=200)
