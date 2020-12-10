import json

from django.http    import JsonResponse
from django.views   import View
from django.core    import serializers
from posting.models import Posts,Comments
from user.models    import Users

from user.utils     import LoginConfirm

class PostsView(View):
    @LoginConfirm
    def post(self, request):
        
        data = json.loads(request.body)
        
        try :
            user = request.user
            post_item = Posts.objects.create(author = user, 
                                             title = data["title"],
                                             image_url = data["image_url"]
                                             )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)
        
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)
        
        except Users.DoesNotExist:
            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 400)

    def get(self, request):
            
        try :

            posts = serializers.serialize("json",Posts.objects.all())
 
            return JsonResponse({'data' : posts}, status = 200)

        except Posts.DoesNotExist:

            return JsonResponse({'MESSAGE': "POST_NOT_FOUND"}, status = 404)


class CommentsView(View):
    @LoginConfirm
    def post(self, request,posting_pk):

        try: 

            data = json.loads(request.body)
            Comments.objects.create(
                author  = request.user,
                content = data['content'],
                post    = Posts.objects.get(id = posting_pk)
            )

            return JsonResponse({"MESSAGE": "SUCCESS"},status=201)
    
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)
        
        except Users.DoesNotExist:
            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 400)
        
        except Posts.DoesNotExist:           
            return JsonResponse({"MESSAGE" : "POST_NOT_FOUND"}, status = 404)
    
    def get(self, request,posting_pk):
        
        if posting_pk == "":
            comments_data = Comments.objects.values()
        else:
            comments_data = Comments.objects.filter(post=int(posting_pk)).values()

        
        return JsonResponse({"Comments":list(comments_data)}, status=200)

class LikesView(View):
    @LoginConfirm
    def post(self, request, posting_pk):
        try:
            post = Posts.objects.get(id = posting_pk)

            if not request.user in post.likes.all():

                post.likes.add(request.user)            
                return JsonResponse({"MESSAGE":"SUCCESS"},status = 201)

            else:                
                return JsonResponse({"MESSAGE":"ALREADY_CHECKED"},status=400)

        except Posts.DoesNotExist:
            
            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status = 400)

    @LoginConfirm
    def delete(self, request, posting_pk):

        try:

            post = Posts.objects.get(id = posting_pk)
        
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return JsonResponse({"MESSAGE":"SUCCESSFULLY DISLIKED"}, status=200)
            else:
                return JsonResponse({"MESSAGE":"DID U REALLY Like THIS POST?"}, status =400)

        except Posts.DoesNotExist:

            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status = 400)
