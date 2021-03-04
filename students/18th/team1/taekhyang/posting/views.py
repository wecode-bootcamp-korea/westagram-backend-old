import json
import re
from json.decoder import JSONDecodeError

from django.views    import View
from django.http     import JsonResponse
from .models         import Posting, PostingImage
from utils.debugger  import debugger


TEST_USER_ID = 1

class UploadView(View):
    def post(self, request):
        try:
            data      = request.body
            json_data = json.loads(data)

            created_time = data['created_time']
            image_url    = data['image_url']










        except KeyError:
            return False
        except JSONDecodeError:
            return False



