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

class ShowView(View):    
    def get(self, request):
        shows  = Posting.objects.all()
        result = []
    
        for show in shows:
            my_dict = {
                'update_time' : show.upload_time,
                'img_url'     : show.img_url,
                'user'        : show.user.email,
            }
            result.append(my_dict)
            
        return JsonResponse({"result" : result}, status=200)
