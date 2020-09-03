import json

from django.http   import JsonResponse
from django.views  import View
from .models       import Posting
from user.models   import User

class PostUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        writer_user = User.objects.get(name = data['writer'])
        if data['writer'] == writer_user.name:
            Posting(
                writer_id   = writer_user.id,
                contents = data['contents'],
                img_url  = data['img_url']
            ).save()
        return JsonResponse({"message":"SUCCESS"}, status=201)

    def get(self, request):
        posting_data = Posting.objects.values()
        return JsonResponse({'writer':list(posting_data)}, status=200)
