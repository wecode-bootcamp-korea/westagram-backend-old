import json

from django.views   import View
from django.http    import JsonResponse

from .models        import Posting, Comment
from user.models    import User
from user.utils     import check_user

class PostingView(View):
    @check_user
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:
            user_model = User.objects.get(id=user)
            Posting.objects.create(user=user_model, post_content=data["post_content"], image_url=data["image_url"])

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
        posts = Posting.objects.all()
        post_list = [{
            "name"    : post.user.name,
            "image"   : post.image_url,
            "content" : post.post_content,
            "time"    : post.time
        } for post in posts]

        return JsonResponse({"post": post_list}, status=200)

class CommentView(View):
    @check_user
    def post(self, request):
        try:
            data            = json.loads(request.body)
            user_id         = request.user
            comment_user    = User.objects.get(id=user_id)
            comment_posting = Posting.objects.get(id=data["posting_id"])
            Comment.objects.create(comment_posting=comment_posting, comment_user=comment_user, comment_content=data["comment_content"])

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    def get(self, request):
        comments = Comment.objects.all()
        comment_list = [{
            "comment_posting" : comment.comment_posting.post_content,
            "comment_user"    : comment.comment_user.name,
            "comment_time"    : comment.comment_time,
            "comment_content" : comment.comment_content
        }for comment in comments]

        return JsonResponse({"post": comment_list}, status=200)
