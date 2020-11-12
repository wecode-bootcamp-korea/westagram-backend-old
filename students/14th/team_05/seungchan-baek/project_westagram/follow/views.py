import json

from django.views     import View
from django.http      import JsonResponse, request

class FollowView(View):
    def post(self, request):
        data = json.loads(request.body)
        # 미완성

