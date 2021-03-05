import json
import re
from json.decoder import JSONDecodeError

from django.views    import View
from django.http     import JsonResponse
from .models         import Posting, PostingImage
from account.models  import User

from utils.debugger  import debugger


TEST_USER_ID = 5

class UploadView(View):
    def post(self, request):
        try:
            data      = request.body
            json_data = json.loads(data)

            image_url = json_data['image_url']
            content   = json_data['content']

            # temporary test User object
            user = User.objects.filter(id=TEST_USER_ID).first()
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            posting = Posting.objects.create(user=user, content=content)
            
            if type(image_url) == list:
                for img in image_url:
                    PostingImage.objects.create(image_url=img, posting=posting)
            else:
                PostingImage.objects.create(image_url=image_url, posting=posting)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        return JsonResponse({'message': 'SUCCESS'}, status=200)


class ShowAllPostingView(View):
    def get(self, request):
        postings      = Posting.objects.all()
        postings_info = list()
        for posting in postings:
            user_email   = posting.user.email
            images       = posting.postingimage_set.all()
            
            image_urls = list()
            for image in images:
                image_urls.append(image.image_url)

            content      = posting.content
            created_time = posting.created_time

            posting_info = dict(user_email=user_email,
                                image_urls=image_urls,
                                content=content,
                                created_time=created_time,
                                )
            postings_info.append(posting_info)
        return JsonResponse(postings_info, status=200, safe=False)
