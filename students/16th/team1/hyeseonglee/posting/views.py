import json
import re
from django.http             import JsonResponse
from django.views            import View
from django.utils.decorators import method_decorator


from posting.models          import Post, Comment, Like
from user.models             import User
# from decorator.utils         import login_decorator,
from decorator.utils         import LoginConfirm

auth = [LoginConfirm,]

# @method_decorator(auth, name='dispatch')
class PostView(View):       
    @LoginConfirm
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            
            title      = data['title']
            content    = data['content']
            image_url  = data['image_url']

            p = re.compile('^([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))$')

            if not title and content and image_url:
                return JsonResponse({'MESSAGE': "YOUR REQUEST IS NOT ADEQUATE!"},status=400)
            
            if not Post.objects.filter(title=title).exists():
                Post.objects.create(
                                    user      = user, 
                                    title     = title,
                                    content   = content,
                                    image_url = image_url,
                                    )
                return JsonResponse({'MESSAGE': 'POST REQUEST SUCCEEDED!'}, status=200)
            return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

    @LoginConfirm
    def get(self, request):
        try:
            posts  = Post.objects.all()
            post_list = []

            for i in posts:
                post_list.append(
                     {
                        'posts.id'        :i.id,
                        'posts.user'      :i.user.email,
                        'posts.title'     :i.title,
                        'posts.content'   :i.content,
                        'posts.created'   :i.created_dt,
                        'posts.image_url' :i.image_url,
                    }
                )
            return JsonResponse({'RESULT':post_list }, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

class PostCommentView(View):
    @LoginConfirm
    def post(self, request,*args, **kwargs):
        try:
            data    = json.loads(request.body)

            user    = User.objects.get(email=data['email'])
            post    = Post.objects.get(title=data['post'])

            content = data['content']
            title   = data['title']
            
            if  not Comment.objects.filter(title=title) and content :
                Comment.objects.create(
                    user    = user,
                    post    = post,
                    author  = email,
                    title   = title,
                    content = content,
                )
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': '동일 제목No! 내용 입력 해주세요!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)   
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)
    @LoginConfirm
    def get(self, request, pk,*args, **kwargs):
        try:
            post     = Post.objects.get(pk=pk)
            comments = post.comment_set.all()

            if not comments.exists():
                return JsonResponse({"MESSAGE":'댓글이 없습니다'}, status=200)
            
            comment_list = []
            for i in comments:
                comment_list.append(
                    {
                        'comment.id'            : i.id,
                        'comment.user.id'       : i.user.id,
                        'comment.post.id'       : post.id,
                        'comment.user.email'    : i.user.email,
                        'comment.title'         : i.title,
                        'comment.content'       : i.content,
                        'comment.created'       : i.created_dt,
                    },
                )
            return JsonResponse({'댓글': comment_list },status=200) # JsonResponse안에 리스트를 넣어줘야합니다!
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)

        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)


class PostLikeView(View):
    @LoginConfirm
    def post(self,request,pk,*args, **kwargs):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email=data['email'])
            post = Post.objects.get(pk=pk)

            if not Like.objects.filter(user=user, post=post).exists(): # 없는 경우
                Like.objects.create(user=user, post=post)
                post.like_num += 1
                post.save()
                return JsonResponse({"MESSAGE": '이 게시물이 좋아요.'}, status=201)
            else:                                                      # 있는 경우
                Like.objects.filter(user=user, post=post).delete()
                post.like_num -= 1
                post.save()
            return JsonResponse({"MESSAGE": "좋아요를 취소 했어요."}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': '이메일을 입력해주세요.'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': '이메일과 찾으려는 게시글 정보를 올바르게 입력해주세요.'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS'}, status=400)   
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS'}, status=400)
            
    @LoginConfirm
    def get(self,request,pk): 
        try:
            like    = Like.objects.get(pk=pk)
            if not like:
                return JsonResponse({'MESSAGE':'좋아요한 사람이 없어요'}, status=200)

            like_info_list = [
                {   'like'                : str(like),
                    'like.created_dt'     : like.created_dt,
                    'like.post.like_num'  : like.post.like_num,
                }
            ]
            return JsonResponse({'MESSAGE':LIKE}, status=200)
            
        except Like.DoesNotExist:
            return JsonResponse({'MESSAGE':'해당 게시물의 좋아요 정보가 아직 존재하지 않아요.'}, status=400)
