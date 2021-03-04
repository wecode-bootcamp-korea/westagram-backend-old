import json
import re
from json.decoder import JSONDecodeError

from django.views    import View
from django.http     import JsonResponse
from .models         import Posting, PostingImage
from account.models  import User

from utils.debugger  import debugger


TEST_USER_ID = 1

class UploadView(View):
    def post(self, request):
        try:
            data      = request.body
            json_data = json.loads(data)

            image_url    = data['image_url']
            
            # temporary test User object
            user = User.objects.filter(id=TEST_USER_ID).exists()
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            posting = Posting(user=user)
            for img in image_url:
                posting_images = PostingImage(image_url=img, posting=posting)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        return JsonResponse({'message': 'SUCCESS'}, status=200)
