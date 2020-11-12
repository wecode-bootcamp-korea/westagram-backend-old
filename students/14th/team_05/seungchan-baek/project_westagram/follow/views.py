import json

from django.views import View
from django.http  import JsonResponse, request

from .models      import Follow
from user.models  import User

class FollowingView(View):
    def post(self, request):
        data = json.loads(request.body)
        followed = User.objects.get(id = data['followed_id'])
        follower = User.objects.get(id = data['follower_id'])

        Follow.objects.create(be_followed = followed, follower = follower)

        return JsonResponse({"message" : "SUCCESS"}, status = 201)

