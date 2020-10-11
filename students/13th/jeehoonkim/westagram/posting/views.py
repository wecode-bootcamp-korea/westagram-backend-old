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
        all_contents = Posting.objects.all().values('user__name', 'content', 'image', 'created_date')
        # 바로 all_contents를 넣으면 에러. 리스트로 넣어야 출력됨. why?
        return JsonResponse({'Postings': list(all_contents)}, status=200)

    def delete(self, request, posting_id):
        data    = json.loads(request.body)
        user_id = data['user_id']
        posting = get_object_or_404(Posting, pk=posting_id)

        if posting.user_id == int(user_id):
            posting.delete()
            return JsonResponse({'message': 'DELETED'}, status=200)
        else:
            return JsonResponse({'message': 'NO PERMISSION'}, status=400)
    
    def put(self, request, posting_id):
        data          = json.loads(request.body)
        user_id       = data['user_id']
        content       = data['content']
        image         = data['image']
        modified_date = timezone.now()
        posting       = Posting.objects.filter(id=posting_id)

        if posting[0].user_id == int(user_id):
            posting.update(content = content, image = image, modified_date = modified_date)
            return JsonResponse({'message': 'EDITED'}, status=200)
        else:
            return JsonResponse({'message': 'NO PERMISSION'}, status=400)

class CommentView(View):
    def post(self, request, posting_id):
        data         = json.loads(request.body)
        posting      = get_object_or_404(Posting, pk = posting_id)
        user_id      = data['user_id']
        content      = data['content']
        thread_to    = data['comment_id']
        created_date = timezone.now()
        
        try:
            User.objects.get(id = user_id)
            if thread_to:
                posting.comment_set.create(
                    user_id      = user_id,
                    thread_to    = thread_to,
                    content      = content,
                    created_date = created_date
                )
            else:
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

    def delete(self, request):
        data       = json.loads(request.body)
        user_id    = data['user_id']
        comment_id = data['comment_id']
        comments   = Comment.objects.get(id=comment_id)

        if comments.user_id == int(user_id):
            comments.delete()
            return JsonResponse({'message': 'DELETED'},status=200)
        else:
            return JsonResponse({'message': 'NO PERMISSION'}, status=400)

    def put(self, request):
        data          = json.loads(request.body)
        user_id       = data['user_id']
        comment_id    = data['comment_id']
        content       = data['content']
        modified_date = timezone.now()
        comments      = Comment.objects.filter(id=comment_id)
        
        if comments[0].user_id == int(user_id):
            comments.update(content=content, modified_date = modified_date)
            return JsonResponse({'message': 'EDITED'}, status=200)
        else:
            return JsonResponse({'message': 'NO PERMISSION'}, status=400)

class LikeView(View):
    def post(self, request, posting_id):
        data    = json.loads(request.body)
        posting = get_object_or_404(Posting, pk=posting_id)
        user_id = data['user_id']
        user    = User.objects.get(id=user_id)

        if user in posting.like.all():
            posting.like.remove(user_id)
            return JsonResponse({'message': 'CANCELED LIKE'}, status=201)
        else:
            posting.like.add(user_id)
            return JsonResponse({'message': 'LIKED'}, status=201)    
