import json

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models      import (
    User
)
from posting.models    import (
    Posting
)

class PostingView(View): #로그인 데코레이터 
    def get(self, request):
        postings = Posting.objects.all()

        posting_list = []

        for posting in postings:
            posting_list.append(
                {
                "username" : posting.username,
                "image_url" : posting.image_url,
                "created_at" : posting.created_at,
                "description" : posting.description
                }
            )
            return Json

    def post(self, request):
        data = json.loads(request.body)

        try:
            image_url    = data['image_url']
            description  = data.get('description', None) #null=True
            username     = data['username']
            user         = User.objects.get(username=username)

            if user.username != username:
                return JsonResponse({"message" : "INVALID_USER"})

            Posting.objects.create(
                username     = user,
                description  = description,
                image_url    = image_url
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            

class PostingDetailView(View):
    pass
