import json, re

from django.views import View
from django.http  import JsonResponse

from user.models import User
from .models     import Post, Comment
from utils       import login_required


class GetPostView(View):
    def get(self, request):
        posts  = Post.objects.all()
        
        results = []
        for post in posts:
            post_dict = {
                "user"      : post.user.email,
                "image"     : post.image_url,
                "content"   : post.content,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }  
            results.append(post_dict)
            
        return JsonResponse({"results": results}, status=200)
    

class PostingView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)

            # 사용자가 보낸 정보를 각 변수에 담기
            user_id    = request.user.id
            image_url  = data["image_url"]
            content    = data["content"]

            # if not :
            #     return JsonResponse({"message": "로그인을 해야 게시물을 등록할 수 있습니다."}, status=401)
            if not image_url:
                return JsonResponse({"message": "이미지를 등록해주세요"}, status=400)
            if not content:
                return JsonResponse({"message": "게시물을 등록해주세요"}, status=400)
            
            # user = User.objects.get(email=user_email) # User클래스의 인스턴스

            Post.objects.create(user_id=user_id, image_url=image_url, content=content)

            return JsonResponse({"message": "SUCCESS"}, status=200)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({"message": "데이터가 없거나 Key값이 적절하지 않습니다."}, status=500)

        except KeyError:
            return JsonResponse({"message": "데이터가 없거나 Key값이 적절하지 않습니다."}, status=500)

        
        except AttributeError:
            return JsonResponse({"message": "값을 입력해주세요."}, status=500)


class CommentView(View):
    @login_required
    def post(self, request):
        
        try:
            data = json.loads(request.body)

            user_email = data["user"]
            post_id    = data["post_id"]
            comment    = data["comment"]
            
            if not user_email:
                return JsonResponse({"message": "로그인을 해야 댓글을 작성할 수 있습니다."}, status=401)
            
            if User.objects.filter(email=user_email).exists() == False:
                return JsonResponse({"message": "당신에 대한 회원정보가 존재하지 않습니다."}, status=401)

            if not comment:
                return JsonResponse({"message": "댓글을 작성해주세요."}, status=401)

            if Post.objects.filter(id=post_id).exists() == False:
                return JsonResponse({"message": "게시물이 존재하지 않습니다."}, status=404)
            

            user = User.objects.get(email=user_email)
            post = Post.objects.get(id=post_id)

            Comment.objects.create(user=user, post=post, comment=comment)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({"results": "Success"}, status=200)


class ShowCommentsView(View):
    def get(self, request, post_id):
        try:            
            post     = Post.objects.get(id=post_id)
            comments = Post.objects.get(id=post_id).comment_set.all()
            
            comment_list = []
            for i, comment in enumerate(comments):
                comment_info = {
                    "comment_writer": comment.user.email,
                    "post_image"    : post.image_url,
                    "post_content"  : post.content,
                    f"comment_{i+1}": comment.comment,
                    "created_at"    : comment.created_at,
                }    

                comment_list.append(comment_info)

            return JsonResponse({"results": comment_list})
        except:
            return JsonResponse({"message": "존재하지 않는 게시물입니다."}, status=400)