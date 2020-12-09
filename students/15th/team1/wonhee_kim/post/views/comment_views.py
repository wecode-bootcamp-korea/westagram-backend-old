import json

from django.http      import JsonResponse
from django.views     import View

from post.models      import Comment, Post
from user.utils       import login_required


class CreateCommentView(View):
    # 1. 인증
    @login_required
    def post(self, request):
        print("================= 댓글 작성 절차 기동 =================")

        # 2. 필수 값 검사
        try:
            content    = json.loads(request.body)['content']
            post_id    = json.loads(request.body)['post_id']
            check_post = Post.objects.filter(id=post_id).exists()
            if not check_post:
                return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=400)
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 3. DB 에 저장
        try:
            Comment.objects.create(
                # user_id  = request.user_id
                user       = request.user,
                post_id    = post_id,
                content    = content,
            )
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "INVALID_PAYLOAD"}, status=400)

        # 4. 모든 과정 통과 -> 201 리턴
        print("================= 댓글 작성 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


class ReadCommentView(View):
    # 1. 인증
    @login_required
    def get(self, request):
        print("================= 댓글 읽기 절차 기동 =================")

        # 2. 필수값 검사
        try:
            post_id    = json.loads(request.body)['post_id']
            check_post = Post.objects.filter(id=post_id).exists()
            if not check_post:
                return JsonResponse({"MESSAGE": "POST DOES NOT EXIST"}, status=400)
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 3. DB 에서 댓글 해당 post_id 에 대한 댓글 불러오기
        comment_list_dict = {}
        comment_list      = Comment.objects.filter(post_id=post_id)
        comment_list      = comment_list.all()
        for comment in comment_list:
            comment_list_dict[f'{comment.id}'] = {'user_nick_name': f'{comment.user.nick_name}',
                                                  'content'       : f'{comment.content}',
                                                  'created_at'    : f'{comment.created_at}',
                                                  }

        # 4. 댓글 목록 및 200 리턴
        print("================= 댓글 읽기 정상 종료 =================")
        return JsonResponse({'MESSAGE'     : 'SUCCESS',
                             'COMMENT_LIST': comment_list_dict
                             }, status=200)
