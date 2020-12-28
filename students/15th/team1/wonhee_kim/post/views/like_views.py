import json

from django.http      import JsonResponse
from django.views     import View

from post.models  import Post, User
from user.utils   import login_required


class _LikeDuplicationError(ValueError):
    pass


class LikeView(View):
    @login_required
    def post(self, request):

        liker = request.user
        try:
            post_id = json.loads(request.body)['post_id']
            like_target_post = Post.objects.get(id=post_id)
            # 중복 검사
            if like_target_post.liker.filter(id=liker.id).exists():
                raise _LikeDuplicationError

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"})
        except Post.DoesNotExist:
            return JsonResponse({"MESSAGE": "POST_DOES_NOT_EXIST"}, status=404)
        except _LikeDuplicationError:
            return JsonResponse({"MESSAGE": "LIKE_DUPLICATION"}, status=400)

        like_target_post.liker.add(liker)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)



