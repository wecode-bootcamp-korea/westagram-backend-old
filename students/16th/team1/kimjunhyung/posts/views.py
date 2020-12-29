import json

from django.views   import View
from django.http    import JsonResponse

from .models            import Post, Comment
from users.models       import User
from decorators.utils   import check_blank, login_required


class PostCreateView(View):
    @check_blank
    @login_required
    def post(self, request):
        data        = json.loads(request.body)
        email       = data["email"]
        content     = data["content"]
        image_url   = data["image_url"]
    
        user = User.objects.filter(email = email)
        Post.objects.create(user = user[0], content = content, image_url = image_url)
        return JsonResponse({"message":"SUCCESS"}, status = 200)
        
class PostView(View):
    def get(self, request):
        posts   = Post.objects.all()
        data    = [
            {   
                "post_id"               : post.id,
                "content"               : post.content,
                "user_email"            : post.user.email,
                "created_at"            : post.created_at,
            }
            for post in posts
        ]
        
        return JsonResponse({"data":data, "first_comment":first_comment}, status = 200)
    

class CommentCreateView(View):
    @check_blank
    @login_required
    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            comment_user_email  = data["email"]
            content             = data["content"]
            post                = Post.objects.get(id = post_id)
            user                = User.objects.get(email = comment_user_email)

            Comment.objects.create(user = user, content = content, post = post)
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except Post.DoesNotExist:
            return JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 404)

class CommentView(View):
    @check_blank
    def get(self, request, post_id):
        post        = Post.objects.get(id = post_id)
        comments    = Comment.objects.filter(post = post)
        
        data = [
            {
                "post_id"           : post_id,
                "comment_content"   : comment.content,
                "comment_user"      : comment.user.email,
                "created_at"        : comment.created_at
            }
            for comment in comments
        ]
        return JsonResponse({"message":"SUCCESS", "data":data}, status = 200)


