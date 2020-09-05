import json 

from django.views import View
from django.http  import JsonResponse

from .models      import Users, Posting, Commenting

class RegisterView(View):
    def post(self, request): 
        data = json.loads(request.body)
        if Users.objects.filter(name=data['user']):
            user_ = Users.objects.get(name=data['user'])
            Posting.objects.create(
                    user       = user_,
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
            'message':list(posts)}, status = 200)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        if Users.objects.filter(name=data['user']) and \
            Posting.objects.filter(image_url=data['image_url']):
            user_ = Users.objects.get(name=data['user'])
            image_url_  = Posting.objects.get(image_url=data['image_url'])
            Commenting.objects.create(
                    user = user_,
                    image_url = image_url_,
                    comment_contents = data['comment'])
            return JsonResponse({
                'message':'SUCCESS'}, status = 200)
        else:
            return JsonResponse({
                'message':'UNAUTHORISED USER'}, status = 401)

    def get(self,request,image_url_id):
        comments = Commenting.objects.values().filter(image_url_id=image_url_id)
        return JsonResponse({
            'message': list(comments)}, status = 200)
