import json

from django.http    import JsonResponse
from django.views   import View
from django.core    import serializers
from posting.models import Posts,Comments
from user.models    import Users

class PostsView(View):

    def post(self, request):
        
        data = json.loads(request.body)
        
        try :
            user = Users.objects.get(email = data['user'])
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

    def post(self, request):

        try: 

            data = json.loads(request.body)
            Comments.objects.create(
                author  = Users.objects.get(email = data['author']),
                content = data['content'],
                post    = Posts.objects.get(id = data['post'])
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
            comments_data = Comments.objects.filter(post=int(slug)).values()

        
        return JsonResponse({"Comments":list(comments_data)}, status=200)
