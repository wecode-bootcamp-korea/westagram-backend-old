import json

from django.views import View
from django.http  import JsonResponse, request

from user.models    import User
from posting.models import Post

class PostUploadView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user    = data['user']
            img_url = data['img_url']

            user = User.objects.get(email=user)

            if Post.objects.filter(user=user, img_url=img_url):
                return JsonResponse({'message':'IMAGE ALREADY EXISTS'}, status=400)

            Post.objects.create(
                user    = user,
                img_url = img_url
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        except Exception as e:
            print(e)