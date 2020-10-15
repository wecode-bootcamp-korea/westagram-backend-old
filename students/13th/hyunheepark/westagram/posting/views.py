import json

from django.views   import View
from django.http    import JsonResponse

from posting.models import Post,Comment
from user.models    import User


class PostView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            user_id = data['user_id']
            content = data['content']
            img_url = data['img_url']
       
            if not img_url:
                 return JsonResponse({'Message':'이미지를 첨부하세요.'},status=400)
            
            Post.objects.create(
                user_id = user_id,
                content = content,
                img_url = img_url
            )
        
            return JsonResponse({'message':'SUCCESS'},status=201)
        except KeyError:
            return JsonResponse({'message':'Key_Error'},status=400)

    def get(self,request):
        return JsonResponse({'post list':list(Post.objects.values())},status=200)

class CommentView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            
            Comment.objects.create(
                    user_id = data['user_id'],
                    comment_content = data['comment_content'],
                    post_id = data['post_id'],
                    )
            return JsonResponse({'message':'SUCCESS'},status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
        except ValueError:
            return JsonRecponse({'message':'VALUE_ERROR'},status=400)

    def get(self,request):
        comment_values = Comment.objects.values()
        first_post = Post.objects.all()[0]
        comments = Comment.objects.filter(post_id = first_post.id).values(
            'user_id',
            'comment_content',
            'created_at'
            )

        return JsonResponse({'message':list(comments)},status=201)
            
