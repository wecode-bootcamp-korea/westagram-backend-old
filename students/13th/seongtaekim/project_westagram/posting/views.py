import json
from django.http     import JsonResponse 
from django.views    import View  
from user.models     import User
from posting.models  import Post, Image_urls, Comment, Like

class PostView(View):
    
    def post(self, request) :
        data    = json.loads(request.body)
        user_id = User.objects.get(user_name=data['user_name'])
        post_id = Post.objects.create(
                contents = data['content'],
                user     = user_id
            ) 
        for image_url in data['image_url'] :
            Image_urls.objects.create(
                image_url = image_url,
                post      = post_id
            )
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
    
    def get(self, request) :
        post_all  = Post.objects.values('id','contents','time','user__user_name')
        post_list = []
        for post in post_all :
            image_urls = Image_urls.objects.filter(post=post['id'])
            post['image_url'] =[image.image_url for image in image_urls]
            post_list.append(post)
        return JsonResponse({'post_all' :post_list}, status=201) 

class CommentView(View) :

    def post(self, request) :
        data      = json.loads(request.body)
        post      = data['post_id']
        contents  = data['contents']
        user_name = data['user_name']

        user_id = User.objects.get( user_name = user_name )
        post_id = Post.objects.get( id = post)
        Comment.objects.create(user=user_id, post=post_id, contents=contents)
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    def get(self, request, post_id) :
        comments = Comment.objects.filter(post = post_id).values('user__user_name', 'contents', 'time')
        return JsonResponse({'MESSAGE': list(comments) }, status=201)

class LikeView(View) :
    def post(self, request) :
        try :
            data    = json.loads(request.body)
            user_id = User.objects.get(id = data['user_id'])
            post_id = Post.objects.get(id = data['post_id'])
            return JsonResponse({'MESSAGE':'Like_success'}, status=201)
            like_check = Like.objects.get(user=user_id,post=post_id)
            like_check.delete()
            return JsonResponse({'MESSAGE':'Like_cancel'}, status=201)
        except KeyError :
            return JsonResponse({'MESSAGE':'KeyError'}, status=401)
        except Like.DoesNotExist :
            Like.objects.create(user=user_id,post=post_id)
            return JsonResponse({'MESSAGE':'Like_success'}, status=201)
        except Post.DoesNotExist :
            return JsonResponse({'MESSAGE':'None_exist_post'}, status=201)
        except User.DoesNotExist :
            return JsonResponse({'MESSAGE':'None_exist_user'}, status=201)
class DeleteView(View) :
    
    def post(self, request) :
        data = json.loads(request.body)
        try :           
            post_id = Post.objects.get(id = data['post_id'])
            post_id.delete()
            return JsonResponse({'MESSAGE':'Success'}, status=201)
        except KeyError :
            return JsonResponse({'MESSAGE':'KeyError'}, status=401)
        except Post.DoesNotExist :
            return JsonResponse({'MESSAGE':'post non-existant'}, status=401)