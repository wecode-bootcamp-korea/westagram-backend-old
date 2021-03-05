import json

from django.views import View
from django.http  import JsonResponse

from .models        import Posting
from account.models import User

class PostingView(View):
    def post(self, request):
        #딕셔너리 모양으로 받아들여진 정보(httpie에 입력한 정보)
        data    = json.loads(request.body)
        user    = User.objects.get(email=data['email'])
        posting = Posting.objects.create(
            img_url = data["img_url"],
            user    = user
            #Time은 알아서 import, 입력 필요 없음.
        )
        return JsonResponse({"message" : "SUCCESS"}, status=200)