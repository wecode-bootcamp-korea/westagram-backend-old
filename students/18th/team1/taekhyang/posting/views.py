import json
import re
from json.decoder import JSONDecodeError

from django.views    import View
from django.http     import JsonResponse
from .models         import Posting, PostingImage, Comment, PostingLike
from account.models  import User

from utils.debugger   import debugger
from utils.decorators import auth_check


class PostingUploadView(View):
    @auth_check
    def post(self, request):
        try:
            data      = request.body
            json_data = json.loads(data)

            user_id   = request.user.id
            image_url = json_data['image_url']
            content   = json_data['content']

            # temporary test User object
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            posting = Posting.objects.create(user=user, content=content)
            
            if type(image_url) == list:
                for img in image_url:
                    PostingImage.objects.create(image_url=img, posting=posting)
            else:
                PostingImage.objects.create(image_url=image_url, posting=posting)
            return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class ShowAllPostingView(View):
    @auth_check
    def get(self, request):
        user_id       = request.user.id
        postings      = Posting.objects.all()

        postings_dict = dict()
        postings_dict['results'] = list()

        for posting in postings:
            username     = posting.user.username
            content      = posting.content
            created_time = posting.created_time
            like_count   = posting.liked_users.count()
            posting_id   = posting.id

            # if the user already did like the posting, it returns 1
            already_like = 1 if PostingLike.objects.filter(user_id=user_id).exists() else 0

            # image_url list
            images   = posting.postingimage_set.all()            
            image_urls = list()
            for image in images:
                image_urls.append(image.image_url)

            # comments list
            comments = Comment.objects.filter(posting=posting)
            comments_list = list()
            for comment in comments:
                username     = comment.user.username
                created_time = comment.created_time
                content      = comment.content
                comment_id   = comment.id

                comment_info = dict(username=username,
                                    created_time=created_time,
                                    content=content,
                                    comment_id=comment_id)
                comments_list.append(comment_info)

            posting_info = dict(username=username,
                                image_urls=image_urls,
                                content=content,
                                created_time=created_time,
                                like_count=like_count,
                                posting_id=posting_id,
                                already_like=already_like,
                                comments=comments_list
                                )
            postings_dict['results'].append(posting_info)
        return JsonResponse(postings_dict, status=200)


class CommentRegisterView(View):
    @auth_check
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id    = request.user.id
            posting_id = data['posting_id']
            content    = data['content']

            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            posting = Posting.objects.filter(id=posting_id).first()
            if not posting:
                return JsonResponse({'message': 'INVALID_POSTING'}, status=400)

            comment = Comment.objects.create(content=content, user=user, posting=posting)
            return JsonResponse({'message': 'SUCCESS', 'comment_id': comment.id}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class ShowCommentView(View):
    """
    comments per single posting  
    """
    @auth_check
    def get(self, request):
        data = json.loads(request.body)

        posting_id = data['posting_id']
        posting = Posting.objects.get(id=posting_id)
        
        comments = Comment.objects.filter(posting=posting)
        if not comments:
            return JsonResponse({'message': 'NO_COMMENT'}, status=400)

        comments_dict = dict()
        comments_dict.setdefault('results', list())

        for comment in comments:
            user         = comment.user.email
            created_time = comment.created_time
            content      = comment.content
            comment_id   = comment.id
            
            comment_info = dict(user=user,
                                created_time=created_time,
                                content=content,
                                content_id=content_id)

            comments_dict['results'].append(comment_info)
        return JsonResponse(comments_dict, status=200)


class PostingLikeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            # TODO: get posting_id and user_id from 'data'
            posting_id = POSTING_ID
            user_id    = TEST_USER_ID
            like       = data['like']

            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=400)

            posting = Posting.objects.filter(id=posting_id).first()
            if not posting:
                return JsonResponse({'message': 'INVALID_POSTING'}, status=400)

            if like == 'like':
                posting.liked_users.add(user)
            elif like == 'unlike':
                posting.liked_users.remove(user)
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class ShowPostingLikeCountView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)
            
            posting_id = POSTING_ID
            posting    = Posting.objects.filter(id=posting_id).first()

            if not posting:
                return JsonResponse({'message': 'INVALID_POSTING'}, status=400)
            
            like_count = posting.liked_users.count()
            result     = dict(like_count=like_count)
            return JsonResponse(result, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class DeletePosingCommentView(View):
    @auth_check
    def post(self, request):
        try:
            data = json.loads(request.body)

            comment_id = data.get('comment_id')
            comment    = Comment.objects.get(id=comment_id)
            comment.delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'COMMENT_DOES_NOT_EXIST'}, status=400)
