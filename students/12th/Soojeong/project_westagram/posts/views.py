import json
from django.http import JsonResponse
from django.views   import View
from user.models import Users
from .models import Posts

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)        
    
        Posts(
            image_url   = data['image_url'],
            pub_date    = data['pub_date'],
            user        = Users.objects.get(id=data['user']),
            pub_content = data['pub_content'],
        ).save()

        return JsonResponse({'message':'CREATED'}, status=201)

class PostDetailView(View):
    def get(self, request):
        data = json.loads(request.body)

        post_data = Posts.objects.filter(id=data['id'])

        return JsonResponse(
            {'post_detail': list(post_data)}, status=200) 
            # 에러발생 
            # TypeError: Object of type Posts is not JSON serializable