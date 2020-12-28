import json

from django.http      import JsonResponse
from django.views     import View

from post.models      import Comment, Post
from user.utils       import login_required


class CommentView(View):
    @login_required
    def post(self, request):
        try:
            content = json.loads(request.body)['content']
            post_id = json.loads(request.body)['post_id']
            # comment 가 달릴 게시물이 존재하는지 확인
            post    = Post.objects.get(id=post_id)

            Comment.objects.create(
                user       = request.user,
                post       = post,
                content    = content,
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_DOES_NOT_EXIST'}, status=404)
        except Comment.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


    @login_required
    def get(self, request):
        try:
            post_id = json.loads(request.body)['post_id']
            Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"MESSAGE": "POST_DOES_NOT_EXIST"}, status=400)

        # DB 에서 댓글 해당 post_id 에 대한 댓글 불러오기
        comment_list_dict = {}
        comment_list      = Comment.objects.filter(post_id=post_id).all()
        for comment in comment_list:
            comment_list_dict[f'{comment.id}'] = {'user_nick_name': f'{comment.user.nick_name}',
                                                  'content'       : f'{comment.content}',
                                                  'created_at'    : f'{comment.created_at}',
                                                  }

        return JsonResponse({'MESSAGE'     : 'SUCCESS',
                             'COMMENT_LIST': comment_list_dict
                             }, status=200)


    @login_required
    def put(self, request):
        try:
            content    = json.loads(request.body)['content']
            comment_id = json.loads(request.body)['comment_id']
            comment    = Comment.objects.get(id=comment_id)

            comment.content = content
            comment.save()

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'MESSAGE': 'COMMENT_NOT_EXIST'}, status=404)
        except Comment.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


    @login_required
    def delete(self, request):
        try:
            comment_id = json.loads(request.body)['comment_id']
            # 사용자가 작성한 comment 가 맞는지 확인
            comment = Comment.objects.get(id=comment_id, user=request.user)

            comment.delete()
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
        except Comment.DoesNotExist:
            return JsonResponse({"MESSAGE": "COMMENT_DOSE_NOT_EXIST"}, status=404)
        except Comment.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
