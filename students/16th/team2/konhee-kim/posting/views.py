import json
import re

from django.http  import JsonResponse
from django.views import View

from user.utils import login_required
# from posting.models  import # specify models


class PostingView(View):
    @login_required
    def post(self, request):
        #data = json.loads(request.body)
        #print(request.headers["Authorization"].split(' ').pop())
        #print(data)

        return JsonResponse({'MESSAGE': 'LOGINED'})

class SeeAllArticlesView(View):
    
    def get(self, request):
        print("get!!")
