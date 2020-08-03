import json

from django.views import View
from django.http import JsonResponse, HttpResponse

from User.models import User
from .models import Post

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(name = data['name'])
        Post(
            name    = user,
            image   = data['image'],
            content = data['content']
        ).save()

    def get(self, request):
        posting_data = Post.objects.values()
        return JsonResponse(
            {"positng_data":list(posting_data)},
            status = 200
        )
