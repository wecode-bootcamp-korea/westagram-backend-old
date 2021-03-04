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

    def get(self, request):
        try:
            data      = request.body
            json_data = json.loads(data)

        except:
            pass 