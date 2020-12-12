import json

from django.http      import JsonResponse
from django.views     import View
from django.utils     import timezone
from django.shortcuts import get_object_or_404

from post.models  import Post
from user.utils   import login_required


class LoadAllPostView(View):
    @login_required
    def get(self, request):

        post_list_dict = {}
        post_list      = Post.objects.all()
        for post in post_list:
            post_list_dict[f'{post.id}'] = {'user_nick_name': f'{post.user.nick_name}',
                                            'content'       : f'{post.content}',
                                            'image_url'     : f'{post.image_url}',
                                            'likes'         : f'{post.liker.count()}',
                                            'created_at'    : f'{post.created_at}',
                                            }

        return JsonResponse({'MESSAGE'  : 'SUCCESS',
                             'POST_LIST': post_list_dict},
                            status=200)


class PostView(View):
    @login_required
    def post(self, request):
        try:
            image_url    = json.loads(request.body)['image_url']
            content      = json.loads(request.body)['content']
            Post.objects.create(
                user       = request.user,
                image_url  = image_url,
                content    = content,
                created_at = timezone.now()
            )
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Post.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


    @login_required
    def get(self, request):
        try:
            post_id = json.loads(request.body)['post_id']
            post = Post.objects.get(id=post_id)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_NOT_EXIST'}, status=404)

        post_dict = {f'{post.id}': {'user_nick_name': f'{post.user.nick_name}',
                                    'content'       : f'{post.content}',
                                    'image_url'     : f'{post.image_url}',
                                    'likes'         : f'{post.liker.count()}',
                                    'created_at'    : f'{post.created_at}',
                                    }}

        return JsonResponse({'MESSAGE': 'SUCCESS', 'POST': post_dict}, status=200)


    @login_required
    def put(self, request):
        try:
            post_id        = json.loads(request.body)['post_id']
            post           = Post.objects.get(id=post_id, user=request.user)
            post.content   = json.loads(request.body)['content']
            post.image_url = json.loads(request.body)['image_url']
            post.save()
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_NOT_EXIST'}, status=404)
        except Post.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

    # delete
    @login_required
    def delete(self, request):
        try:
            post_id = json.loads(request.body)['post_id']

            # 삭제 요청한 post 에 대해 사용자가 작성한 것인지 확인
            post = Post.objects.get(id=post_id, user=request.user)

            post.delete()
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POST_NOT_EXIST'}, status=404)
        except Post.IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
















