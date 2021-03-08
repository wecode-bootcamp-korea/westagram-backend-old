import json

from django.views import View
from django.http  import JsonResponse

from .models        import Follow
from account.models import User


class FollowView(View):
    def post(self, request):
        data = json.loads(request.body)
