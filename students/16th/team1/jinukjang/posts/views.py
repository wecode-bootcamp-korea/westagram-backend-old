import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post, PostImage, Comment, Like
from users.models import User


class CreatePostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data['username'])

            # 동일한 제목의 Post생성 불가능. -> CommentView에서 Post의 title로 접근할거임.
            if Post.objects.filter(title=data['title']).exists():
                return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400) 

            post = Post.objects.create(
                title   = data['title'],
                content = data['content'],
                writer  = user
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
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD USER"},status = 400)
        

class PostView(View):
    def get(self, request):
        try:
            posts = Post.objects.all()
            post_list = []

            for post in posts:
                images = post.postimages.all()
                likes = post.likes.all().count()

                img_list = [img.img_url for img in imges]

                post_dict = {
                    'writer'    : post.writer.username,
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


# Post의 title입력
class CommentView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            post = Post.objects.get(title=data['title'])

            comment = post.comments.all()

            return JsonResponse({'posts':list(comment)},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD POST"},status = 400)

class CreateCommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            Comment.objects.create(
                user    = User.objects.get(username = data['username']),
                post    = Post.objects.get(title    = data['title']),
                content = data['content'],
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD USER"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD POST"},status = 400)

        
class PostLikeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data['username'])
            post = Post.objects.get(title=data['title'])

            if  Like.objects.filter(user=user, post=post).exists():
                Like.objects.filter(user=user, post=post).delete()
                return JsonResponse({'MESSAGE':'POST_LIKE_CANCLE'}, status=200)

            Like.objects.create(user=user, post=post)
            return JsonResponse({'MESSAGE':'POST_LIKE'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD USER"},status = 400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD POST"},status = 400)
