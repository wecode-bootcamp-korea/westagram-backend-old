import json

from django.views       import View
from django.http        import JsonResponse

from .models            import Post, Comment, Like, CommentByComment
from users.models       import User
from decorators.utils   import check_blank, login_required, get_user
        
class PostView(View):
    def get(self, request):
        posts       = Post.objects.all()
        comments    = Comment.objects.select_related("post")
        data = [
            {   
                "post_id"               : post.id,
                "content"               : post.content,
                "user_email"            : post.user.email,
                "created_at"            : post.created_at,
                "first_comment_content" : post.comment_set.all().order_by("-created_at")[0].content 
                                        if comments.filter(post = post).exists() 
                                        else "댓글을 추가해주세요" ,
                "first_comment_user"    : post.comment_set.all().order_by("-created_at")[0].user.email     
                                        if comments.filter(post = post).exists()
                                        else "" 
            }
            for post in posts
        ]
        return JsonResponse({"data" : data}, status = 200)

class PostCreateView(View):
    @check_blank
    @login_required
    def post(self, request):
        token       = json.loads(request.headers.get("Token"))
        user        = get_user(token)
        content     = data["content"]
        image_url   = data["image_url"]
    
        Post.objects.create(user = user, content = content, image_url = image_url)
        return JsonResponse({"message":"SUCCESS"}, status = 200)

class PostLikeView(View):
    @login_required
    def post(self, request):
        data        = json.loads(request.body)
        post_id     = data["post_id"]
        token       = json.loads(request.headers.get("Token"))
        user        = get_user(token)
        post        = Post.objects.get(id = post_id)
        check_like  = Like.objects.filter(user = user, post = post).select_related("user").select_related("post")

        if check_like.exists():
            Like.objects.filter(user = user, post = post).delete()
            return JsonResponse({"message":"USER_CANCLE_LIKE"}, status = 200)
        Like.objects.create(user = user, post = post)
        return JsonResponse({"message":"USER_LIKE_POST"}, status = 200)

class PostUpdateView(View):
    @check_blank
    @login_required
    def put(self, request, post_id):
        data        = json.loads(request.body)
        token       = json.loads(request.headers.get("Token"))
        user        = get_user(token)
        content     = data['content']
        image_url   = data['image_url']

        try:
            post        = Post.objects.filter(id = post_id)
            owner       = User.objects.prefetch_related("post_set").filter(post = post[0])[0]
            if user == owner:
                post.update(user = owner, content = content, image_url = image_url)
                return JsonResponse({"message":"SUCCESS"}, status = 200)
            return JsonResponse({"message":"PERMISSION_DENIED"}, status = 403)
        except Post.DoesNotExist:
            return JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 400)

class PostDeleteView(View):
    @login_required
    def delete(self, request):
        data    = json.loads(request.body)
        token   = json.loads(request.headers.get("Token"))
        user    = get_user(token)
        post_id = data['post_id']
        post    = Post.objects.filter(id = post_id)
        
        if not post.exists():
            return JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 400)
        if not user == post[0].user:
            return JsonResponse({"message":"PERMISSION_DENIED"}, status = 403)
            
        post[0].delete()
        return JsonResponse({"message":"POST_DELETE"}, status = 200)

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
        return JsonResponse({"data" : data}, status = 200)

class CommentCreateView(View):
    @check_blank
    @login_required
    def post(self, request, post_id):
        try:
            data        = json.loads(request.body)
            content     = data["content"]
            post        = Post.objects.get(id = post_id)
            token       = json.loads(request.headers.get("Token"))
            user        = get_user(token)

            Comment.objects.select_related("user").create(user = user, content = content, post = post)
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except Post.DoesNotExist:
            return JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 404)

class CommentDeleteView(View):
    @login_required
    def delete(self, request, post_id, comment_id):
        token   = json.loads(request.headers.get("Token"))
        user    = get_user(token)
        post    = Post.objects.filter(id = post_id)
        if not post.exists():
            return JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 400)

        comment = Comment.objects.filter(id = comment_id, post = post[0]).select_related("post")
        if not comment.exists():
            return JsonResponse({"message":"COMMENT_DOES_NOT_EXIST"}, status = 400)

        owner   = User.objects.filter(comment = comment[0]).prefetch_related("comment_set")[0]   
        if user == owner:
            comment[0].delete()
            return JsonResponse({"message":"COMMENT_DELETED"}, status = 200)
             
class CommentAddComment(View):
    @check_blank
    @login_required
    def post(self, request, post_id, comment_id):
        data    = json.loads(request.body)
        token   = json.loads(request.headers.get("Token"))
        user    = get_user(token)
        content = data['content']
        post    = Post.objects.filter(id = post_id)
        comment = Comment.objects.filter(id = comment_id).select_related("post")

        if not post.exists():
            JsonResponse({"message":"POST_DOES_NOT_EXIST"}, status = 400)
        if not comment.exists():
            JsonResponse({"message":"COMMENT_DOES_NOT_EXIST"}, status = 400)
        post        = post[0]
        comment     = comment[0]
        comments    = post.comment_set.all()

        if comment in comments:
            CommentByComment.objects.create(user = user, content = content, comment = comment)
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        return JsonResponse({"message":"NO_COMMENT_ON_THE_POST"}, status = 400)