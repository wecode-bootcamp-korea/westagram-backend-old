import json
import re

from django.shortcuts import get_object_or_404
from django.views     import View
from django.http      import JsonResponse
from django.utils     import timezone

from .models          import Posting, Comment
from user.models      import User

class PostingView(View):
    def post(self, request):
        data         = json.loads(request.body)
        user_id      = data['user_id']
        content      = data['content']
        image        = data['image']
        created_date = timezone.now()

        if image:
            Posting.objects.create(
                user_id      = user_id,
                content      = content,
                image        = image,
                created_date = created_date
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        else:
            return JsonResponse({'message': 'PLEASE UPLOAD IMAGE'})
        
    def get(self, request):
        all_contents=Posting.objects.all().values('user__name', 'content', 'image', 'created_date')

        return JsonResponse({'Postings': list(all_contents)}, status=200)
        
class CommentView(View):
    def post(self, request, posting_id):
        data         = json.loads(request.body)
        posting      = get_object_or_404(Posting, pk = posting_id)
        user_id      = data['user_id']
        content      = data['content']
        created_date = timezone.now()
        try:
            User.objects.get(id = user_id)
            posting.comment_set.create(
                user_id      = user_id,
                content      = content,
                created_date = created_date
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER DOES NOT EXIST'}, status=400)

    def get(self, request, posting_id):
        all_comments = Comment.objects.filter(posting_id=posting_id).values('user__name', 'content', 'created_date')
        if all_comments:
            return JsonResponse({'Comments': list(all_comments)}, status=200)
        else:
            return JsonResponse({'message': 'DELETED POST'}, status=400)

class LikeView(View):
    def post(self, request, posting_id):
        data=json.loads(request.body)
        posting=get_object_or_404(Posting, pk=posting_id)
        user_id=data['user_id']

        posting.like.add(user_id)
        return JsonResponse({'message': 'LIKED'}, status=201)    
