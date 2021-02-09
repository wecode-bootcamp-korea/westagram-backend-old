import json, re

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Posting, Comment, Like
from user.models        import User
from .utils             import login_decorator

class PostingView(View):
    def get(self, request):
        postings        = Posting.objects.all()
        posting_list    = []

        for posting in postings :
            posting_info = {
                    'name'          : User.objects.get(id=posting.user_id).name,
                    'image_url'     : posting.image_url,
                    'descrption'    : posting.description,
                    'create_at'     : posting.create_at,
                    }
            posting_list.append(posting_info)

        return JsonResponse({'results' : posting_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user

            if not User.objects.get(name=data['name']) == user :
                return JsonResponse({'message' : 'MISMATCH_TOKEN'}, status=400)
            
            if not User.objects.get(name=data['name']).exists() : 
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)
            
            Posting.objects.create(
                    user        = user.id,
                    image_url   = data['image_url'],
                    description = data.get('description', None)
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class PostingDetailView(View):
    @login_decorator
    def get(self, request, user_id):
        try:
            user    = request.user
            posts   = Posting.objects.filter(user_id=user_id)

            if not user.id == user_id :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post_list = []
            for post in posts:
                post_info = {
                        'id' : post.id,
                        'image_url' : post.image_url,
                        'description' : post.description
                        }
                post_list.append(post_info)

            return JsonResponse({'result' : post_list}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def put(self, request, posting_id):
        try:
            data        = json.loads(request.body)
            user        = request.user
            image_url   = data['image_url']
            description = data['description']
            user_id     = user.id

            post = Posting.objects.get(id=posting_id)

            if not user.name == post.user.name :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post.image_url      = image_url
            post.description    = description
            post.save()
            
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POST'}, status=400)
    
    @login_decorator
    def patch(self, request,posting_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            post    = Posting.objects.get(id=posting_id)

            if not user.name == post.user.name :
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)
            
            post.description    = data.get('description', post.description)
            post.image_url      = data.get('image_url', post.image_url)
            post.save()

            return JsonResponse({'result' : 'SUCCESS_EDIT'}, status=200)


        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    @login_decorator
    def delete(self, request, posting_id):
        try:
            user        = request.user

            post = Posting.objects.get(id=posting_id)
            if not user.name == post.user.name:
                return JsonResponse({'message' : 'INVALID_USER'}, status=200)
            post.delete()

            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Posting.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_POST'}, status=400)

class CommentView(View):
    def get(self, request):
        comments = Comment.objects.all()
        comment_list = []
        for comment in comments:
            comment_info={
                    'user' : comment.user.name,
                    'comment' : comment.comment,
                    'posting' : comment.posting.description
                    }
            comment_list.append(comment_info)
        return JsonResponse({'result' : comment_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            comment = data['comment']
            user    = request.user

            Comment.objects.create(
                    comment     = comment,
                    user_id     = user.id,
                    posting_id  = data['posting_id'],
                    parent_id   = data.get('parent_id', None)
                    )
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Exception as e:
            return JsonResponse({'message' : e}, status=400)

class CommentDetailView(View):
    # 특정 게시글의 댓글만 보기
    def get(self, request, posting_id):
        try:
            comments = Comment.objects.filter(posting_id=posting_id)
            comment_list = []
            for comment in comments:
                comment_detail = {
                        'user' : comment.user.name,
                        'comment' : comment.comment,
                        'Up_comment' : comment.parent_id
                        }
                comment_list.append(comment_detail)
            if not comment_list:
                return JsonResponse({'result' : 'NO_COMMENT'}, status=200)

            return JsonResponse({'result' : comment_list}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
    # 특정 게시글의 특정 댓글에 달린 대댓글만 보기
    def get(self, request, comment_id):
        try:
            comments = Comment.objects.filter(parent_id=comment_id)
            comment_list = []
            for comment in comments:
                comment_detail = {
                        'user' : comment.user.name,
                        'comment' : comment.comment,
                        'Up_comment' : comment.parent_id
                        }
                comment_list.append(comment_detail)
            if not comment_list:
                return JsonResponse({'result' : 'NO_COMMENT'}, status=200)

            return JsonResponse({'result' : comment_list}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


    @login_decorator
    def put(self, request, comment_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            comment = Comment.objects.get(id=comment_id)

            if user.id != comment.user_id:
                return JsonResponse({'message' : 'INVALID_RIGHT'}, status=400)

            comment.comment=data['comment']
            comment.save()
            return JsonResponse({'result' : 'SUCCESS_EDIT'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)


    @login_decorator
    def delete(self, request, comment_id):
        try:
            user    = request.user
            comment = Comment.objects.filter(id=comment_id)
            comment.delete()

            return JsonResponse({'result' : 'SUCCESS_DELETE'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'message' : 'NO_EXISTING_COMMENT'}, status=400)

class LikeView(View):
    def get(self, request):
            like_list =[]
            for post in posts:
                like_info = {
                    'posting_id' : post.id,
                    'user_id' : post.user_id
                    }
                like_list.append(like_info)

            return JsonResponse({'result' : like_list}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            posting     = data['posting_id']
            user        = request.user
            post        = Posting.objects.get(id=posting)

            # Posting의 MtoM으로 접근해서 집어넣기!
            post.like_user.add(User.objects.get(id=user.id))
            # Like model을 import한다면 아래의 것을 사용
            #Like.objects.create(user_id=user.id, posting_id=posting)

            return JsonResponse({'result' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class LikeDetailView(View):
    def get(self, request, posting_id):
        try:
            posts       = Like.objects.filter(posting_id=posting_id)
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({'message' : 'INVALID_POST'}, status=400)

            posting_like =[]
            for post in posts:
                posting_like_info = {
                    'posting_id' : post.id,
                    'user_id' : post.user_id
                    }
                posting_like.append(posting_like_info)

            # 좋아요 수가 하나도 없을 경우
            if not posting_like:
                return JsonResponse({'result' : 'NONE_HEART'}, status=200)

            return JsonResponse({'result' : len(posting_like)}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, posting_id):
        try:
            user        = request.user
            like        = Like.objects.get(user_id=user.id, posting_id=posting_id)

            like.delete()
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except Like.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_LIKE'}, status=400)
