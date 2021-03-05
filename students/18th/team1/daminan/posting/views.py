import json

from django.views import View
from django.http  import JsonResponse

from .models import Posting

class PostingView(View):
    def post(self, request):
        data    = json.loads(request.body)
        user    = Posting.objects.get(email=data['email'])
        posting = Posting.objects.create(
            time    = data["time"],
            img_url = data["img_url"],
            user    = user
        )
        return JsonResponse({"message" : "SUCCESS"}, status=200)