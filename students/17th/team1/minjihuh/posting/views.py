import json

from django.http       import JsonResponse, HttpResponse
from django.views      import View
from django.db.models  import Q

from user.models       import (
    User
)
from posting.models    import (
    Posting,
    Comment,
    Like
)

from westagram.utils   import login_decorator

class PostingView(View): 
    @login_decorator
    def get(self, request):
        try: 
            postings = Posting.objects.all()

            posting_list = [] 

            for i in range(len(postings)):
                posting_list.append( 
                    {
                    "image_url" : postings[i].image_url,
                    "description" : postings[i].description,
                    "username" : request.user.username.username,
                    "created_at" : postings[i].created_at,
                    }
                )
            return JsonResponse({"data" : posting_list}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)   

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            image_url    = data['image_url']
            description  = data.get('description', None) #null=True
            username     = request.user.username 
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
    @login_decorator
    def get(self, request):
        try:
            # comments = Comment.objects.all()
            comments   = Comment.objects.filter(id=13)

            comment_list = [] 

            for comment in comments:
                comment_list.append( 
                    {
                    "comment_username"   : request.user.username,
                    "text"               : comment.text,
                    "posting_photo"      : comment.posting_photo.id,
                    "created_at"         : comment.created_at,
                    "root"               : comment.root_id
                    }
                )
            return JsonResponse({"data" : comment_list}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @login_decorator    
    def post(self,request): 
        data = json.loads(request.body)

        try:
            user_id          = request.user.id
            comment_username = User.objects.get(id=user_id)
            text             = data['text']
            posting_id       = data['posting']
            root_id          = data.get('root', None)

            if text == "":
                return JsonResponse({"message" : "TEXT_FIELD_REQUIRED"}, status=400)

            if posting_id == "":
                return JsonResponse({"message" : "INVALID_IMAGE"}, status=400)
            
            # if not Comment.objects.filter(id=root_id):
            #     return JsonResponse({"message" : "INVALID_COMMENT"}, status=400)

            posting_photo = Posting.objects.get(id=posting_id)

            root          = Comment.objects.filter(root_id=root_id)[0].id 

            Comment.objects.create( 
                comment_username = comment_username,
                text             = text,
                posting_photo    = posting_photo,
                root             = Comment.objects.get(id=root)
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class LikeView(View):
    @login_decorator
    def get(self, request):
        try:
            likes = Like.objects.all()
            like_list = []

            for like in likes:
                like_list.append(
                    {
                        "like_username" : request.user.username,
                        "posting_photo" : like.posting_photo.id,
                        "liked_at"    : like.liked_at

                    }
                )
                return JsonResponse({"data" : like_list}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            user_id       = data.get(request.user, None)
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
    @login_decorator
    def patch(self, request, posting_id):
        data = json.loads(request.body)
        
        try:
            if Posting.objects.filter(id=posting_id):
                posting               = Posting.objects.get(id=posting_id)

                username_id           = User.objects.get(id=data.get('user.User', posting.username.id))
                posting.username.id   = username_id
                posting.image_url     = data.get('image_url', posting.image_url)
                posting.description   = data.get('description', posting.description)

                posting.save()

                if request.user != username_id:
                    return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)
                
                return JsonResponse({"message" : "SUCCESS"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message" : "REQUEST_BODY_IS_MANDATORY"}, status=400)  

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  

    @login_decorator
    def delete(self, request, posting_id):
        try:
            if Posting.objects.filter(id=posting_id).exists():
                user_id    = request.user
                posting    = Posting.objects.get(id=posting_id)

                if user_id != posting.username.id:
                    return JsonResponse({"message" : "INVALID_USER"}, status=400)

                Posting.objects.filter(id=posting_id).delete()
                return HttpResponse(status=200)

            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  

class CommentDetailView(View):
    @login_decorator  
    def delete(self, request, comment_id):
        try:
            if Comment.objects.filter(id=comment_id).exists():
                user_id  = request.user
                comment  = Comment.objects.get(id=comment_id)

                if user_id != comment.comment_username:
                    return JsonResponse({"message" : "INVALID_USER"}, status=400)

                Comment.objects.filter(id=comment_id).delete()
                return HttpResponse(status=200)

            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)  
