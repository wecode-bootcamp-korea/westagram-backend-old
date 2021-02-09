import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models      import (
    User
)
from posting.models    import (
    Posting,
    Comment,
    Like
)

from westagram.utils   import login_decorator

class PostingView(View): 
    # @login_decorator #로그인 데코레이터 테스트하기
    def get(self, request):
        postings = Posting.objects.all()

        posting_list = [] 

        for i in range(len(postings)):
            posting_list.append( 
                {
                "image_url" : postings[i].image_url,
                "description" : postings[i].description,
                "username" : postings[i].username.username,
                "created_at" : postings[i].created_at,
                }
            )
        return JsonResponse({"data" : posting_list}, status=201)

    def post(self, request):
        data = json.loads(request.body)

        try:
            image_url    = data['image_url']
            description  = data.get('description', None) #null=True
            username     = data['username']
            user         = User.objects.get(username=username)

            if user.username != username:
                return JsonResponse({"message" : "INVALID_USER"})

            Posting.objects.create(
                username     = user,
                description  = description,
                image_url    = image_url
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)            

class CommentView(View):
    def get(self, request):
        try:
            # comments = Comment.objects.all()
            comments   = Comment.objects.filter(id=1)

            comment_list = [] 

            for comment in comments:
                comment_list.append( 
                    {
                    "comment_username"   : comment.comment_username.username,
                    "text"               : comment.text,
                    "posting_photo"      : comment.posting_photo.id,
                    "created_at"         : comment.created_at
                    }
                )
            return JsonResponse({"data" : comment_list}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
    def post(self,request): 
        data = json.loads(request.body)
        #나는 url과 username을 원하지 일반 id를 원하지 않아.. 
        try:
            user_id          = data['username']
            comment_username = User.objects.get(id=user_id)
            text             = data['text']
            posting_id       = data['posting']

            if text == "":
                return JsonResponse({"message" : "TEXT_FIELD_REQUIRED"})

            if posting_id == "":
                return JsonResponse({"message" : "INVALID_IMAGE"})

            posting_photo = Posting.objects.get(id=posting_id)

            Comment.objects.create( 
                comment_username = comment_username,
                text             = text,
                posting_photo    = posting_photo,
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class LikeView(View):
    def get(self, request):
        try:
            likes = Like.objects.all()
            like_list = []

            for like in likes:
                like_list.append(
                    {
                        "like_username" : like.like_username.username,
                        "posting_photo" : like.posting_photo.id,
                        "liked_at"    : like.liked_at

                    }
                )
                return JsonResponse({"data" : like_list}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id       = data.get('username', None)
            posting_id    =  data.get('posting', None)
            
            if User.objects.filter(id=user_id).exists():
                like_username = User.objects.get(id=user_id)

                if Posting.objects.filter(id=posting_id).exists():
                    posting_photo =  Posting.objects.get(id=posting_id)

                    Like.objects.create(
                        like_username = like_username,
                        posting_photo = posting_photo,
                    )
                    
                    return JsonResponse({"message" : "SUCCESS"}, status=200)

                return JsonResponse({"message" : "INVALID_POST"}, status=400)

            return JsonResponse({"message" : "INVALID_USER"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  

    # unlike 구현해야함       

class PostingDetailView(View):
    def patch(self, request, posting_id):
        data = json.loads(request.body)
        if Posting.objects.filter(id=posting_id):
            posting               = Posting.objects.get(id=posting_id)

            username_id           = User.objects.get(id=data.get('user.User', posting.username.id))
            posting.username.id   = username_id
            posting.image_url     = data.get('image_url', posting.image_url)
            posting.description   = data.get('description', posting.description)

            posting.save()

            return JsonResponse({"message" : "SUCCESS"}, status=201)

    def delete(self, request, posting_id):
        if Posting.objects.filter(id=posting_id).exists():
            Posting.objects.filter(id=posting_id).delete()
            return HttpResponse(status=200)
        return JsonResponse({"message" : "INVALID_APPROACH"})

class CommentDetailView(View):
    def post(self, request, posting_id, root_id):
        data = json.loads(request.body)

    def delete(self, request, comment_id):
        if Comment.objects.filter(id=comment_id).exists():
            Comment.objects.filter(id=comment_id).delete()
            return HttpResponse(status=200)

        return JsonResponse({"message" : "INVALID_APPROACH"})
