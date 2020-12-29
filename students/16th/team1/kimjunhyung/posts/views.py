import json

from django.views   import View
from django.http    import JsonResponse

from .models            import Post, Comment
from users.models       import User
from decorators.utils   import check_blank


class PostCreateView(View):
    @check_blank
    def post(self, request):
        data        = json.loads(request.body)
        email       = data["email"]
        content     = data["content"]
        image_url   = data["image_url"]
        
        user = User.objects.filter(email = email)
        if user.exists():
            Post.objects.create(user = user[0], content = content, image_url = image_url)
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        return JsonResponse({"message":"LOGIN_REQUIRED"}, status = 400)
        
class PostView(View):
    def get(self, request):
        posts   = Post.objects.all()
        data    = [
            {   
                "post_id"       : post.id,
                "content"       : post.content,
                "user_email"    : post.user.email,
                "created_at"    : post.created_at,
            }
            for post in posts
        ]
        return JsonResponse({"data":data}, status = 200)

