import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post, PostImage, Comment, Like
from users.models import User


class CreatePostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User()
            if   'username' in data:
                user = User.objects.get(username=data['username'])
            elif 'email'    in data:
                user = User.objects.get(email=data['email'])
            elif 'phone'    in data:
                user = User.objects.get(phone=data['phone'])

            # 동일한 제목의 Post생성 불가능.
            if Post.objects.filter(title=data['title']).exists():
                raise KeyError                

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
            except:
                pass
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200) 
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

        

class PostView(View):
    def get(self, request):
        try:
            posts = Post.objects.all()
            post_list = []

            for post in posts:
                imges    = post.postimage_set.all()
                img_list = [img.img_url for img in imges]

                post_dict = {
                    'writer'    : post.writer.email or post.writer.username or post.writer.phone,
                    'title'     : post.title,
                    'content'   : post.content,
                    'img'       : img_list,
                    'created_at': post.created_at,
                    'updated_at': post.updated_at,
                }

                post_list.append(post_dict)

            return JsonResponse({'menus':post_list},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)


# Post의 title입력
class CommentView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            post = Post.objects.get(title=data['title'])

            return JsonResponse({'menus':list(comment_data)},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

# username, email, phone와 Post의 title 입력
class CreateCommentView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User()
            if   'username' in data:
                user = User.objects.get(username=data['username'])
            elif 'email'    in data:
                user = User.objects.get(email=data['email'])
            elif 'phone'    in data:
                user = User.objects.get(phone=data['phone'])

            Comment.objects.create(
                user    = user,
                post    = Post.objects.get(title=data['title']),
                content = data['content'],
            )

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200) 
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

        
# username, email, phone와 Post의 title 입력
class PostLikeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User()

            # 요청시 username, email, phone로 User 찾기
            if   'username' in data:
                user = User.objects.get(username=data['username'])
            elif 'email'    in data:
                user = User.objects.get(email=data['email'])
            elif 'phone'    in data:
                user = User.objects.get(phone=data['phone'])
            
            post = Post.objects.get(title=data['title'])

            if  Like.objects.filter(user=user, post=post).exists():
                Like.objects.filter(user=user, post=post).delete()
                post.count_likes-=1
                post.save()
                return JsonResponse({'MESSAGE': 'POST_LIKE_CANCLE'}, status=200)

            Like.objects.create(user=user, post=post)
            post.count_likes+=1
            post.save()
            return JsonResponse({'MESSAGE': 'POST_LIKE'}, status=200) 

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)