import json
from json.decoder import JSONDecodeError

from django.http  import JsonResponse
from django.views import View

from posting.models import Posting, Image, Comment, Like
from user.models    import User
from user.utils     import login_decorator

class PostingView(View):
    @login_decorator
    def post(self, request):
        try :
            data = json.loads(request.body)
            user = request.user

            content        = data.get('content', None)
            image_url_list = data.get('image_url', None)

            if not (content and image_url_list):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            posting = Posting.objects.create(
                writer  = user.username,
                content = content,
                user    = user
            )

            for image_url in image_url_list:
                Image.objects.create(
                    image_url = image_url,
                    posting   = posting
                ) 

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
    
    def get(self, request):
        posting_list = [{
            "writer"    : posting.writer,
            "content"   : posting.content,
            "image_url" : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
            "create_at" : posting.created_at
            } for posting in Posting.objects.all()
        ]

        return JsonResponse({'data':posting_list}, status=200)


class PostingSearchView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)

            username = data.get('username', None)

            if not username:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not User.objects.filter(username=username).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)

            posting_list = [{
                "writer"    : posting.writer,
                "content"   : posting.content,
                "image_url" : [i.image_url for i in Image.objects.filter(posting_id=posting.id)],
                "create_at" : posting.created_at
                } for posting in Posting.objects.filter(writer=username)
            ]

            return JsonResponse({'data':posting_list}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

class CommentView(View):
    @login_decorator
    def post(self, request):
        try :
            data = json.loads(request.body)
            user = request.user

            content = data.get('content', None)
            posting_id = data.get('posting_id', None)

            if not (content and posting_id):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':"POSTING_DOES_NOT_EXIST"}, status=404)
            
            posting = Posting.objects.get(id=posting_id)
            
            comment = Comment.objects.create(
                writer  = user.username,
                content = content,
                user    = user,
                posting = posting
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

    def get(self, request):
        try:
            data = json.loads(request.body)

            posting_id = data.get('posting_id', None)

            if not posting_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=404)

            comment_list = [{
                "writer"    : comment.writer,
                "content"   : comment.content,
                "create_at" : comment.created_at
                } for comment in Comment.objects.filter(posting_id=posting_id)
            ]

            return JsonResponse({'data':comment_list}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)


class LikeView(View):
    @login_decorator
    def post(self, request):
        try :
            data = json.loads(request.body)
            user = request.user

            posting_id = data.get('posting_id', None)

            if not posting_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':"POSTING_DOES_NOT_EXIST"}, status=404)
            
            posting = Posting.objects.get(id=posting_id)
            
            like = Like.objects.create(
                user    = user,
                posting = posting
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

    def get(self, request):
        try:
            data = json.loads(request.body)

            posting_id = data.get('posting_id', None)

            if not posting_id:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message':'POSTING_DOES_NOT_EXIST'}, status=404)
            
            user_list     = [i.user_id for i in Like.objects.filter(posting_id=posting_id)]
            username_list = [User.objects.get(id=i).username for i in user_list]
            posting       = Posting.objects.get(id=posting_id)

            like_list = {
                "username" : username_list,
                "likes"    : len(username_list)
            }

            return JsonResponse({'data':like_list}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

