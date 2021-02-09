import json

from django.http      import HttpResponse, JsonResponse
from django.views     import View

from .models          import Post
from user.models      import Account


class PostView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email = data['email']).exists():
                user = Account.objects.get(email = data['email'])

                Post(
                    user      = user,
                    content   = data['content'],
                    image_url = data['image_url'],
                    ).save()
                
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        except Exception as e:
            return JsonResponse({'MESSAGE' : f'NO {e}'}, status = 400)

    def get(self, request):
        post_list = list(Post.objects.values())

        return JsonResponse({'post_list': post_list}, status=200)

    
