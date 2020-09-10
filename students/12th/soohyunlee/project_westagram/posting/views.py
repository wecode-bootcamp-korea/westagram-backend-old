import json

from django.http   import JsonResponse
from django.views  import View
from .models       import Posting
from user.models   import User

class PostUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        writer_user = User.objects.get(name = data['writer'])

        Posting(
            writer_id = writer_user.id,
            contents  = data['contents'],
            img_url   = data['img_url']
        ).save()
        return JsonResponse({"message":"SUCCESS"}, status=201)

    def get(self, request):
        posting_data = Posting.objects.all()
        posting_list = []
        for posting in posting_data:
            posting_list.append(
                {
                    'contents' : posting.contents,
                    'writer'   : posting.writer.name
                }
            )
        return JsonResponse({'writer':list(posting_data)}, status=200)
