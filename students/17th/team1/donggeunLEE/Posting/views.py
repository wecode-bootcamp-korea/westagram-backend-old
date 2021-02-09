import json

from django.http   import HttpResponse, JsonResponse
from django.views  import View
from django.utils  import timezone

from User.models   import Userinfo
from .models       import UserPosting, UserComment, Userlike, AdditonalComment
from User.utilities import login_decorator


# Mission4
class ContentSignupView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            image_url = data['image_url']
            
            UserPosting.objects.create(
                    user_ID   = user,
                    image_url = image_url
                    )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)

    @login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        user = request.user
        user_id = user.id
        image_url = data['image_url']
        
        if UserPosting.objects.filter(id = user_id, image_url = image_url).exists():
            UserPosting.objects.get(id=user_id, image_url=image_url).delete()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
    
    # Mission9 게시물 수정
    @login_decorator
    def update(self, request, user_id):
        try:
            data = json.loads(request.body)
            user = UserPosting.obejcts.get(id = user_id)
        
            user.image_url = data['image_url']
            user.create_at = timezone.datetime.now()
            user.save()

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)

class GetCommentView(View):
    def get(self, request):
        comment_data = UserComment.objects.values()




class ContentGetView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        result = []
        posts = UserPosting.objects.all()

        for post in posts:
            result.append(
                    {   
                        'user_ID'     : dict(user),
                        'image_url'   : UserPosting.image_url,
                        'posted_time' : UserPosting.create_at
                        }
                    )
        return JsonResponse({"MESSAGE": "SUCCESS", "result" : result}, status=200)
       

# Mission5
class UserCommentView(View):
    def post(self, request):
        try:    
            data = json.loads(request.body)
            if Userinfo.objects.filter(name=data['name']).exists:
                user = Userinfo.objects.get(name=data['name'])
                
                if UserPosting.objects.filter(image_url = data['image']).exists():
                    image = UserPosting.objects.get(image_url=data['image'])

                    UserComment.objects.create(
                            user_id = user,
                            image = image,
                            comment = data['comment']
                            )
                    return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)
                return JsonResponse({"MESSAGE":"INVALID_IMAGE"}, status=400)
            return JsonResponse({"MESSAGE" : "INVALID_NAME"}, status=400)
        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
    
    # Misson8 댓글 제거
    def delete(self, request):
        data = json.loads(request.body)

        if UserComment.objects.filter(comment = data['comment']).exists():
            UserComment.objects.get(comment=data['comment']).delete()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

    def get(self, request):
        comment_data = UserComment.objects.values()

        return JsonResponse({"comment_data": list(comment_data)}, status=200)

class AddCommentView(View):
    @login_decorator
    def post(self, request, comment_id):
        data       = json.loads(request.body)
        user       = request.user
        user_id    = user.id
        comment_id = UserComment.objects.get(id = comment_id)

        AdditonalComment.objects.create(
                comment = comment_id,
                name    = user.name,
                addcomment = data['addcomment']
                )
        return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        

#Mission6 좋아용 구현하기
class UserLikeView(View):
    def post(self, request):
        # 좋아요가 있으면 제거, 없으면 post
        try:
            data = json.loads(request.body)
            user = Userinfo.objects.get(name = data['name'])
            post = UserPosting.object.get(image = data['image'])

            if Userlike.objects.filter(post = post, user=user).exists():
                Userlike.objects.get(post=post, user=user).delete()
                return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
            Userlike.objects.create(
                    post = post,
                    user = user
                    )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"INVALID_KEY"}, status=400)


