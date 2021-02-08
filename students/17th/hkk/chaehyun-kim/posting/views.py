import json, re

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import Posting, Comment, UserLike
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
                return JsonResponse({'message' : '토큰-유저 불일치'}, status=400)
            
            if not User.objects.get(name=data['name']).exists() : 
                return JsonResponse({'message' : '없는 유저'}, status=400)
            
            Posting.objects.create(
                    user        = user.id,
                    image_url   = data['image_url'],
                    description = data.get('description', None)
                    )
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : '누구냐 넌'}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class CommentView(View):
    def get(self, request):
        # 모든 댓글을 보고자 한다면 request.body에 아무것도 안 담으면 된다.
        if not request.body:
            comments = Comment.objects.all()
        
        # 질문 : 이 경우 else 문을 안만들면 comment_list=[]이 그냥 실행되는건지, else 문안에 포함되는 건지 구분할 수 가 있나요??
        
        # 특정 포스팅에 대한 댓글만 보고싶다면 포스팅 id 를 body에 보내주면 된다.
        else:
            data = json.loads(request.body)
            comments = Comment.objects.filter(posting=data['posting_id'])
        # 아직 댓글이 없는 게시글을 선택했을때
            if not Comment.objects.filter(posting_id=data['posting_id']):
                return JsonResponse({'result' : '아직 댓글 없음'}, status=200)
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
            # 이따 테스트할때 data['user_id']대신 user['user_id']로 해보기
            if not User.objects.get(id=data['user_id']) == user :
                return JsonResponse({'message' : '토큰-유저 불일치'}, status=400)

            if not data['user_id'] : 
                return JsonResponse({'message' : '없는 유저'}, status=400)

            Comment.objects.create(
                    comment     = comment,
                    user_id     = data['user_id'],
                    posting_id  = data['posting_id']
                    )
            return JsonResponse({'result' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'메세지' : '왜 키에러?'}, status=400)
        except Exception as e:
            return JsonResponse({'message' : e}, status=400)

class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            posting  = data['posting_id']
            userlike = data['user_id']
            post    = Posting.objects.get(id=posting)


            if not User.objects.get(id=data['user_id']) == userlike :
                return JsonResponse({'message' : '토큰-유저 불일치'}, status=400)
            # Posting의 MtoM으로 접근해서 집어넣기!
            post.userlike.add(UserLike.objects.create(userlike_id=userlike))
            # Like model을 import한다면 아래의 것을 사용
            #Like.objects.create(userlike_id=userlike, posting_id=posting)

            return JsonResponse({'result' : 'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
