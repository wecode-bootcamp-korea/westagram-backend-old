import json

from django.http        import JsonResponse, HttpResponse
from django.shortcuts   import get_object_or_404
from django.views       import View
from django.utils       import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models        import PostModel
from Account.models import User

class Upload(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            upload_user = data['username']
            upload_text = data['text']
            upload_img_url = data['url']
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        try:
            user_class = User.objects.get(username=upload_user)
        except ObjectDoesNotExist: # 게시물을 등록한 유저정보가 데이터베이스에 없음
            return JsonResponse( {"message": "INVALID_USER"}, status=401)

        p = PostModel(
            user = user_class,
            text = upload_text,
            img_url = upload_img_url,
        )

        p.save()
        return JsonResponse({'message':'SUCCESS'}, status=200)
        
class Show(View):
    def get(self, request):
        post_data = PostModel.objects.values()
        return JsonResponse({'post':list(post_data)},status=200)