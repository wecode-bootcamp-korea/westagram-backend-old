import json

from django.core          import serializers
from django.http          import JsonResponse
from django.views.generic import View

from account.models import User
from .models        import Post

class CreatePostView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user_id = data['user_id']
            text    = data['text']
            img_url = data['img_url']

            user = User.objects.get(id=user_id)
            Post(
                user    = user,
                text    = text,
                img_url = img_url,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER_ID'}, status = 400)

class ListPostView(View):
    def get(self, request):
        posts = Post.objects.all()
        serialized_posts = serializers.serialize('json', posts)
        return JsonResponse(serialized_posts, safe = False)
