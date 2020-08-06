import json

from django.views import View
from django.http  import JsonResponse

from .models     import Post, Comment
from user.models import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id = data['user_id']).exists():
                user = User.objects.get(id = data['user_id'])
                Post(
                    user    = user,
                    post    = data['post'],
                    img_url = data['img_url'],
                ).save()
                return JsonResponse({"message" : "SUCCESS"}, status = 200)
            return JsonResponse({"message" : "USER MISMATCH"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status = 400)
        
class PostGetView(View):
    def get(self, request):
        db_post = Post.objects.values()
        return JsonResponse({'data' : list(db_post)}, status = 200)
    
class CommentPostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id = data['user_id']).exists() and Post.objects.filter(id = data['post_id']).exists():
                Comment(
                    user    = User.objects.get(id = data['user_id']),
                    post    = Post.objects.get(id  = data['post_id']),
                    comment = data['comment'],
                ).save()
                return JsonResponse({"message" : "SUCCESS"}, status = 200)
            return JsonResponse({"message" : "USER, POST MISMATCH"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status = 400)
 
class CommentGetView(View):
    def get(self, request):
        db_comment = Comment.objects.values()
        return JsonResponse({'data' : list(db_comment)}, status = 200)
    
    

# # serialize queryset
# serialized_queryset = serializers.serialize('json', posting)
# # serialize object
# serialized_object = serializers.serialize('json', [some_object,])