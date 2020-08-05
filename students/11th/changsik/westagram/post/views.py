import json

from django.views import View
from django.http  import JsonResponse

from .models     import Post
from user.models import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                Post(
                    user    = user,
                    text    = data['text'],
                    img_url = data['img_url'],
                ).save()
            return JsonResponse({"message" : "SUCCESS"}, status = 200)   
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status = 400)
        
    def get(self, request):
        db_post = Post.objects.values()
        return JsonResponse({'data' : list(db_post)}, status = 200)