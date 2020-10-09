import json
import re

from django.views     import View
from django.db.models import Q
from django.http      import JsonResponse
from django.utils     import timezone

from .models          import Posting
from user.models      import User

class PostingView(View):
    def post(self, request):
        data=json.loads(request.body)
        user_id=data['user_id']
        content=data['content']
        image=data['image']
        created_date=timezone.now()

        Posting.objects.create(
            user_id=user_id,
            content=content,
            image=image,
            created_date=created_date
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)
        


