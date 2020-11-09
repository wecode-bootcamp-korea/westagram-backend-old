import json
from django.views import View
from django.http import JsonResponse
from posting.models import Posting


class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            User.objects.get(id=1)

            posting = Posting(
            user      = data["user"],
            time      = data["time"],
            image_url = data["image_url"],
            )
        #
        # Posting.objects.get(id
        # Posting.objects.create()
        #
        # Posting.objects.create(user="1", image="url")

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        # except Exception:
        #     return JsonResponse({'message': 'INVALID_USER'}, status=401)


    def get(self, request):


        return JsonResponse({"Hello":"World"}, status=200)
