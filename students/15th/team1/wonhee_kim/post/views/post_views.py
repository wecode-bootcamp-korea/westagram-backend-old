import json

from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone
from django.shortcuts import get_object_or_404

from post.models  import Post
from user.utils   import login_required


class CreatePostView(View):
    # 1. 인증
    @login_required
    def post(self, request):
        print("================= 포스트 작성 절차 기동 =================")

        # 2. 필수값 검사
        try:
            image_url    = json.loads(request.body)['image_url']
            content      = json.loads(request.body)['content']
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 3. DB에 데이터 작성
        try:
            post           = Post.objects.create(
                # user_id  = request.user_id  id 로 넣거나 객체로 넣거나 둘 다 가능
                user       = request.user,
                image_url  = image_url,
                content    = content,
                created_at = timezone.now()
            )
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "INVALID_PAYLOAD"}, status=400)

        # 4. 모든 과정 통과 -> 201 리턴
        print("================= 포스트 작성 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


class ReadPostView(View):
    @login_required
    def get(self, request):
        print("================= 포스트 출력 절차 기동 =================")

        post_list_dict = {}
        post_list      = Post.objects.all()
        for post in post_list:
            post_list_dict[f'{post.id}'] = {'user_nick_name': f'{post.user.nick_name}',
                                            'content'       : f'{post.content}',
                                            'image_url'     : f'{post.image_url}',
                                            'likes'         : f'{post.liker.count()}',
                                            'created_at'    : f'{post.created_at}',
                                            }
        print("================= 포스트 출력 정상 종료 =================")
        return JsonResponse({'MESSAGE'  : 'SUCCESS',
                             'POST_LIST': post_list_dict},
                            status=200)


class ReadPostDetailView(View):
    @login_required
    def get(self, request, post_id):
        print("================= 포스트 출력 절차 기동 =================")

        post = get_object_or_404(Post, id=post_id)
        post_dict = {f'{post.id}': {'user_nick_name': f'{post.user.nick_name}',
                                    'content'       : f'{post.content}',
                                    'image_url'     : f'{post.image_url}',
                                    'likes'         : f'{post.liker.count()}',
                                    'created_at'    : f'{post.created_at}',
                                    }}

        print("================= 포스트 출력 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS',
                             'POST_LIST': post_dict},
                            status=200)


class DeletePostView(View):
    # 1. 인증
    @login_required
    def get(self, request, post_id):
        print()
        print("================= 게시물 삭제 절차 기동 =================")

        # 2. 사용자가 작성한 post 가 맞는지 확인
        user_id = request.user_id
        post = Post.objects.filter(id=post_id, user_id=user_id)
        if not post.exists():
            print("Error: COMMENT_NOT_FOUND_WITH_THIS_CONDITION")
            return JsonResponse({'MESSAGE': 'COMMENT_NOT_FOUND_WITH_THIS_CONDITION'}, status=404)

        # 3. DB 에서 게시물 데이터 삭제
        try:
            post.delete()
        except Exception as e:
            print(f'Exception: {e}')
            return JsonResponse({"MESSAGE": "POST_CAN_NOT_BE_DELETED"}, status=500)

        # 4. 모든 과정 통과 -> 201 리턴
        print("================= 게시물 삭제 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)



