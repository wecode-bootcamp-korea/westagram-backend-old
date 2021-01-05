import json
from django.http    import JsonResponse
from django.views   import View
from posting.models import Posting
from django.apps    import apps

User = apps.get_model('user', 'User')


class PostingView(View):
    def post(self, request):   
        data    = json.loads(request.body)
        user_db = User.objects.all()
        post=Posting(
            post_id     = User.objects.get(account=data['post_id']),
            post_url    = data['post_url'],
            description = data['description'],
        )
        name=post.post_id.account
        print(name)
        try:
            
            if (data['post_id'] == None) or (data['post_url'] == None):
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

            if not user_db.filter(account = data['post_id']).exists():
                return  JsonResponse({'MESSAGE':'NON EXISTING USER'}, status=400)
            
            post.save()
            
            #return JsonResponse(f"{name}, {post.post_url}, {post.description}")

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
