import json

from django.views    import View
from django.http     import JsonResponse

from .models         import Post, PostImage, Comment, Like
from users.models    import User
from users.decorator import login_decorator


class PostView(View):
    def get(self, request):
        try:
            posts = Post.objects.all()
            post_list = []

            for post in posts:
                images = post.post_images.all()
                likes = post.likes.all().count()

                img_list = [img.img_url for img in images]

                post_dict = {
                    'writer'    : post.writer.email,
                    'title'     : post.title,
                    'content'   : post.content,
                    'img'       : img_list,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at,
                    'cnt_likes' : likes
                }

                post_list.append(post_dict)

            return JsonResponse({'posts':post_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)


class CreatePostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            # 동일한 제목의 Post생성 불가능. -> CommentView에서 Post의 title로 접근할거임.
            if Post.objects.filter(title=data['title']).exists():
                return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400) 

            post = Post.objects.create(
                title   = data['title'],
                content = data['content'],
                writer=request.user
            )

            # img_url 데이터를 콤마로 구분해서 입력받았을 때 리스트로 바꿔주기
            try:
                img_urls = data['img_url'].split(',')

                for img_url in img_urls:
                    PostImage.objects.create(
                        post    = post,
                        img_url = img_url.strip()
                    )
            except: # img_url이 없는 경우.
                pass
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200) 
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

# title로 수정할 Post검색 후 content 수정 가능.
class EditPostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            post = Post.objects.get(
                writer = request.user,
                title  = data['title']
            )

            post.content = data['content']
            post.save()
            return JsonResponse({'MESSAGE':'POST EDIT SUCCESS'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)

class DeletePostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            Post.objects.get(title=data['title'], writer = request.user).delete()
            return JsonResponse({'MESSAGE':"REMOVE POST"},status = 200)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)    
        
class LikePostView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            post = Post.objects.get(title=data['title'])
            like = Like.objects.filter(user=user, post=post)

            if  like:
                like.delete()
                return JsonResponse({'MESSAGE':'POST_LIKE_CANCLE'}, status=200)

            Like.objects.create(user=user, post=post)
            return JsonResponse({'MESSAGE':'POST_LIKE'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)

# Post의 title입력
class CommentView(View):
    def get(self, request):
        try:
            data    = json.loads(request.body)
            post    = Post.objects.get(title=data['title'])
            comment = post.comments.all()
            return JsonResponse({'posts':list(comment)},status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)

# recomment <- comment.id로 입력
class CreateCommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            recomment = Comment.objects.get(id = data['recomment']) if 'recomment' in data else None
            
            Comment.objects.create(
                user      = request.user,
                post      = Post.objects.get(title = data['title']),
                content   = data['content'],
                recomment = recomment
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)

class DeleteCommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            Comment.objects.filter(
                user    = request.user,
                post    = Post.objects.get(title = data['title']),
                content = data['content'],
            ).delete()

            return JsonResponse({'MESSAGE':'REMOVE COMMENT'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID POST"},status = 400)