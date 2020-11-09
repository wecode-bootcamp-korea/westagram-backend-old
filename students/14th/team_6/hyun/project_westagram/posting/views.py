from django.views import View
from .models import Post
from django.http import  JsonResponse
import json
from datetime import datetime
from user.models import User


class Posting(View):
    def post (self,request):
        data = json.loads(request.body)
        user = User.objects.filter(user_name = data["name"] )
        #name = User.objects.get(id=data["name_id"])
#        post = Post.objects.select_related('user_name').get(user_name_id = data['name_id'])
#        name = post.user_name.user_name

 #         if data['title'] == '' or data['name_id'] =='':
 #            return JsonResponse ({ "message : " : "제목을 입력해주세요" }, status = 400 )
 #
 #         if Post.objects.filter(
 #             name, title = data["title"] ) .exists():
 #             return JsonResponse({"message : " : "제목을 적어주세요"} , status = 400)

        if user.exists():
            Post.objects.create(
                user_name = User.objects.get(user_name= data["name"]),
                title = data["title"],
                content = data["content"],
                date = datetime.now(),
                photo = data["photo"]
            )
            return JsonResponse ( { 'message : ' : '게시물 업로드' } , status = 200 )
        else :
            return JsonResponse ({ 'message : ' : '로그인이 필요한 서비스입니다'}, status = 400)

    def get(self, request):
        results = []
        for post in Post.objects.all() :
            results.append(User.objects.values())
            return JsonResponse ({ "data : " :"results" },status = 200)
