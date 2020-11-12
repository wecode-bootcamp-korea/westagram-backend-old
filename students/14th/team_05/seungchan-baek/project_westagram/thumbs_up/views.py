import json

from django.views import View
from django.http  import JsonResponse, request

from .models      import ThumbsUp
from user.models  import User
from post.models  import Posting
from user.utils   import login_decorator


class ThumbsUpView(View):
    def post(self,  request):
        data = json.loads(request.body)
        user = User.objects.get(id = data['user_id'])
        post = Posting.objects.get(id = data['post_id'])
        print(user.id)
        print(post.id)
        print(type(user))
        print(type(post))
        try:
            ThumbsUp(user = user, post = post).save()

            return JsonResponse({'message' : "SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERORR'}, status=400)