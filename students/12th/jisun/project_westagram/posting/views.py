import json 

from django.views import View
from django.http  import JsonResponse

from .models      import Users, Posting 

class RegisterView(View):
    def post(self, request): 
        data = json.loads(request.body)
        if Users.objects.filter(name=data['writer']):
            user_id = Users.objects.get(name=data['writer'])
            Posting.objects.create(
                    writer     = user_id,
                    image_url  = data['image_url'],
                    contents   = data['contents'],
                    )
            return JsonResponse({
                'message':'SUCCESS'}, status = 201)
        else:
            return JsonResponse({
                'message':'UNAUTHORISED USER'}, status = 401)

    def get(self, request):
        posts = Posting.objects.values()
        return JsonResponse({
            'message': list(posts)}, status = 200) 
