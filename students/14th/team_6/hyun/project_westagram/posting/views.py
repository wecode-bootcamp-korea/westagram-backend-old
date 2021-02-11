from django.views import View
from django.http  import JsonResponse
from datetime     import datetime
import json

from .models      import Post
from user.models  import User

class Posting(View):
    def post (self,request):
        data = json.loads(request.body)
        user = User.objects.filter(user_name = data["name"] )
        try:
            if user.exists():
                Post.objects.create(
                    user_name = User.objects.get(user_name = data["name"]),
                    title     = data["title"],
                    content   = data["content"],
                    date      = datetime.now(),
                    photo     = data["photo"],
                    )
                return JsonResponse ( { 'message : ' : '게시물 업로드' } , status = 200 )
        except :
            return JsonResponse ({ 'message : ' : '로그인이 필요한 서비스입니다'}, status = 400)

    def get(self, request):
        data = Post.objects.values()
        return JsonResponse({ "data : " : list(data) }, status = 200 )





