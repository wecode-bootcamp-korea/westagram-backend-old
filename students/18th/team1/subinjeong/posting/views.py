import json

from django.http  import JsonResponse
from django.views import View

from .models     import Posting
from user.models import User


class PostingView(View):
    def post(self,request):   
        try:
            upload_data = json.loads(request.body)

            title       = upload_data['title']
            img_url     = upload_data['img_url']
            user_object = User.objects.get(username=username)

            Posting.objects.create(
                user    = user_object,
                title   = upload_data['title'],
                img_url = upload_data['img_url']
            )
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except:
            return JsonResponse({'message': 'ERROR'}, status = 400)

    def get(self,request):

        posting_objects = Posting.objects.all()
        response = []

        for posting_object in posting_objects:
            dictionarize = (
                {
                    'title'          : posting_object.title,
                    'img_url'        : posting_object.img_url,
                    'time_created'   : posting_object.time_created,
                    'username'       : posting_object.user.username
                }
            )
            response.append(dictionarize)
        return JsonResponse(response, safe=False, status= 200)
