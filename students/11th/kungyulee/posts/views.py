import traceback

from django.views        import View
from django.http         import JsonResponse
from django.forms.models import model_to_dict

from accounts.models import User
from .models         import Post, Comment

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(phone_number=data['phone_number'])
            post = Post(
                author    = user,
                contents  = data['contents'],
                image_url = data['image_url'],
            ).save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : KeyError}, status = 400)

        return JsonResponse({'message' : 'TRY AGAIN'}, status = 400)

    def get(self, request):
        posts     = Post.objects.all().values()
        post_list = list(posts)
        return JsonResponse(post_list, safe = False)

class PostDetailView(View):
    def get(self, request, pk):
        post      = Post.objects.get(pk = pk)
        dict_post = model_to_dict(post)
        return JsonResponse(dict_post, status = 200)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User.objects.get(phone_number=data['phone_number'])
            post = Post.objects.get(pk=data['pk'])
            comment = Comment(
                author   = user,
                post     = post,
                contents = data['contents'],
            ).save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : KeyError}, status = 400)

        return JsonResponse({'message' : 'TRY AGAIN'}, status = 400)

    def get(self, request):
        comments     = Comment.objects.all().values()
        comment_list = list(comments)
        return JsonResponse(comment_list, safe = False)
