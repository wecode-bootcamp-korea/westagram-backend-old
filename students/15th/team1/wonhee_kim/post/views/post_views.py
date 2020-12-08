import json

from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone

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
        post_list      = Post.objects.order_by('created_at')
        for post in post_list:
            post_list_dict[f'{post.id}'] = {'user_nick_name': f'{post.user.nick_name}',
                                            'content'       : f'{post.content}',
                                            'image_url'     : f'{post.image_url}',
                                            'created_at'    : f'{post.created_at}',
                                            }
        print("================= 포스트 출력 정상 종료 =================")
        return JsonResponse({'MESSAGE'  : 'SUCCESS',
                             'POST_LIST': post_list_dict},
                            status=200)
