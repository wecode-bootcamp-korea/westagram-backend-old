import json
import jwt

from django.views import View
from django.http  import JsonResponse, HttpResponse

from . models     import Post
from user.utils   import login_decorator


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data      = json.loads(request.body)
            image_url = data['image_url']
            caption   = data['caption']
            user      = request.user.id

            Post.objects.create(
                    image_url = image_url,
                    caption   = caption,
                    user_id   = user
                    )
            
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


