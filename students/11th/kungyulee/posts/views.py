import traceback, json, jwt

from django.views        import View
from django.http         import JsonResponse
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from accounts.models import User
from .models         import Post, Comment
from .decorators     import is_admin

#payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])

secret = 'abc'

# @method_decorator(is_admin, name = 'dispatch')
class GetToken(View):
    def post(self, request):
        data = json.loads(request.body)
        payload = jwt.decode(data['access_token'], secret, algorithms=['HS256'])
        user = User.objects.get(id = payload['id'])
        return JsonResponse({'user_id' : user.id}, status = 200)

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])
        try:
            user = User.objects.get(id = payload['id'])
            # user = User.objects.get(phone_number=data['phone_number'])
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
        if Post.objects.filter(pk = pk).exists():
            post      = Post.objects.get(pk = pk)
            dict_post = model_to_dict(post)
            return JsonResponse(dict_post, status = 200)
        return JsonResponse({'message' : "post doesn't exist"}, status = 400)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            Comment(
                author   = User.objects.get(phone_number=data['phone_number']),
                post     = Post.objects.get(pk=data['pk']),
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
