import json

from django.http   import HttpResponse, JsonResponse
from django.views  import View

from User.models   import Userinfo
from .models       import UserPosting, UserComment, Userlike
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

class GetCommentView(View):
    def get(self, request):
        comment_data = UserComment.objects.values()

        return JsonResponse({"comment_data": list(comment_data)}, status=200)




# Mission6 좋아용 구현하기
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


