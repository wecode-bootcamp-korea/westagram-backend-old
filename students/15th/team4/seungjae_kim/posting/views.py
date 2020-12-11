import json

from django.http    import JsonResponse
from django.views   import View
from django.core    import serializers
from posting.models import Posts
from posting.models import Comments
from user.models    import Users

from user.utils     import LoginConfirm

class PostsView(View):
    @LoginConfirm
    def post(self, request):
        
        data = json.loads(request.body)
        
        try :
            user      = request.user
            post_item = Posts.objects.create(author    = user, 
                                             title     = data["title"],
                                             image_url = data["image_url"]
                                             )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)
        
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)
        
        except Users.DoesNotExist:
            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)

    def get(self, request):
            
        try :
            posts = list(Posts.objects.values()) 
            return JsonResponse({'data' : posts}, status=200)

        except Posts.DoesNotExist:
            return JsonResponse({'MESSAGE': "POST_NOT_FOUND"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)
    
    @LoginConfirm
    def delete(self, request, posting_pk):
        
        try:
            post = Posts.objects.get(id=posting_pk)
            
            assert post.author.id == request.user.id, "UNAUTHORIZED"
            
            post.delete()
            
            return JsonResponse({"MESSAGE": "SUCCESS"},status=200)

        except Posts.DoesNotExist:
            return JsonResponse({"MESSAGE": "POST_NOT_FOUND"},status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"},status=200)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE": f"{e}"},status=401)

    @LoginConfirm
    def put(self,request,posting_pk):
        
        try:
            data = json.loads(request.body)
            post = Posts.objects.get(id=posting_pk)
            
            assert post.author.id == request.user.id, "UNAUTHORIZED"

            post.title      = data['title']
            post.image_url  = data['image_url']    
            post.save()    
            
            return JsonResponse({"MESSAGE":"SUCCESS"},status=200)
        
        except Posts.DoesNotExist:
            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status=404)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE":f"{e}"},status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"PLZ FOLLOW THE INPUT FORMAT"},status=400)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)

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
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)
    
    def get(self, request,posting_pk):
        
        if posting_pk == "":
            comments_data = Comments.objects.values()
        else:
            comments_data = Comments.objects.filter(post=int(posting_pk)).values()
        
        return JsonResponse({"Comments":list(comments_data)}, status=200)
    
    # 아마 이렇게 하는 것은 비효율적일지도?
    # comment에도 pk가 있는데 구분 짓는데 posting_pk까지 필요할런지..
    # url 패턴을 좀 더 고민해봐야겟다.
    @LoginConfirm
    def delete(self, request, posting_pk, comment_pk):
        
        try:
            comment = Comments.objects.get(id=comment_pk,post=posting_pk)
            
            assert comment.author.id == request.user.id, "UNAUTHORIZED"
            
            comment.delete()
            return JsonResponse({"MESSAGE":"SUCCESS"},status=200)

        except Posts.DoesNotExist:
            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status=404)
        
        except Comments.DoesNotExist:
            return JsonResponse({"MESSAGE":"RESOURCE_NOT_FOUND"},status=404)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE":f"{e}"},status=401)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"PLZ FOLLOW THE INPUT FORMAT"},status=400)

    @LoginConfirm
    def put(self, request, posting_pk, comment_pk):
        
        try:
            data    =   json.loads(request.body)
            comment =   Comments.objects.get(post=posting_pk, id=comment_pk)
            
            assert  comment.author.id ==request.user.id, "UNAUTHORIZED"
            
            comment.content =  data['content']
            comment.save()
            
            return   JsonResponse({"MESSAGE":"SUCCESS"},status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE":"PLZ FOLLOW THE INPUT FORMAT"}, status=400)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)
        
        except Comments.DoesNotExist:
            return JsonResponse({"MESSAGE":"RESOURCE_NOT_FOUND"})
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE": f"{e}"},status=401)
        
class LikesView(View):
    @LoginConfirm
    def post(self, request, posting_pk):
        try:
            post = Posts.objects.get(id = posting_pk)

            if not request.user in post.likes.all():
                post.likes.add(request.user)            
                return JsonResponse({"MESSAGE":"SUCCESS"},status = 201)

            else:                
                return JsonResponse({"MESSAGE":"ALREADY_LIKED"},status=400)

        except Posts.DoesNotExist:
            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status = 400)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)

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
            return JsonResponse({"MESSAGE":"POST_NOT_FOUND"},status = 404)
        
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE": "PLZ FOLLOW THE INPUT FORMAT"}, status=400)



