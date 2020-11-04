import json
from django.http import JsonResponse
from django.views   import View
from user.models import Users
from .models import Posts
from django.forms.models import model_to_dict

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

    def get(self, request):
        data = json.loads(request.body)
        post_data = Posts.objects.filter(id=data['id']).values()
        post_data_1 = list(post_data)

        return JsonResponse( post_data_1[0], status=200 )
            
            