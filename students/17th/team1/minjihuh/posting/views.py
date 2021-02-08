import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models      import (
    User
)
from posting.models    import (
    Posting,
    Comment
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


class PostingDetailView(View):
    pass
