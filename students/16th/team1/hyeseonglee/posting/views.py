import json
import re
from django.http             import JsonResponse
from django.views            import View
from django.utils.decorators import method_decorator


from posting.models          import Post, Comment, Like
from user.models             import User
from decorator.utils         import LoginConfirm


class PostCreateView(View):       
    @LoginConfirm
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            title      = data['title']
            content    = data['content']
            image_url  = data.get('image_url')
            
            if not Post.objects.filter(title=title).exists():                
                Post.objects.create(
                                    user      = user, 
                                    title     = title,
                                    content   = content,
                                    image_url = image_url,
                                    )
                return JsonResponse({'MESSAGE': '게시물 생성 완료' }, status=200)
            return JsonResponse({'MESSAGE': 'TITLE ALREADY EXISTS!'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

class PostReadView(View):  
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

class PostUpdateView(View):  
    @LoginConfirm
    def put(self, request, post_id):
        try:
            data      = json.loads(request.body)
            user      = request.user
            title     = data['title']     
            content   = data['content']     
            image_url = data.get('image_url','None')

            post      = Post.objects.get(id=post_id)
            
            if not post.user.id == user.id:
                return JsonResponse({'MESSAGE': '게시물 수정 권한이 없습니다.'}, status=403)

            post.title     = title
            post.content   = content
            post.image_url = image_url
            post.save()
            return JsonResponse({'MESSAGE': '게시글 수정 완료.'}, status=200) 
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

class PostDeleteView(View):
    @LoginConfirm
    def delete(self, request, post_id):
        try:
            user  = request.user
            post = Post.objects.get(id=post_id) # 삭제하려는 게시물 조회
            if user.id != post.user.id:
                return JsonResponse({'MESSAGE': '게시물 삭제 권한 없음.'}, status=200)

            if post:
                post.delete()
                return JsonResponse({'MESSAGE': '게시물 삭제 완료.'}, status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'게시물이 없습니다.'},status=400)


class CommentCreateView(View):
    @LoginConfirm
    def post(self, request, post_id, *args, **kwargs):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = data['content']
            title   = data['title']
            post    = Post.objects.get(pk=post_id)

            
            if  not Comment.objects.filter(title=title,post_id=post_id, user_id=user.id).exists() :
                Comment.objects.create(
                    user    = user,
                    post    = post,
                    title   = title,
                    content = content,
                )
                return JsonResponse({'MESSAGE': '댓글 생성 완료.'}, status=200)
            return JsonResponse({'MESSAGE': '제목과 내용을 확인해주세요.'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY 에러 발생!'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE 에러!'},status=400)   
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS!'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'POST DOES NOT EXISTS!'},status=400)

class CommentReadView(View):
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

class CommentUpdateView(View):  
    @LoginConfirm
    def put(self, request, post_id, comment_id):
        try:
            data      = json.loads(request.body)
            user      = request.user
            title     = data['title']     
            content   = data['content']     
            post_id   = Post.objects.get(id=post_id)
            comment   = Comment.objects.get(post_id=post_id,id=comment_id)
            
            if not comment.user.id == user.id:
                return JsonResponse({'MESSAGE': '댓글 수정 권한이 없습니다.'}, status=403)

            comment.title     = title
            comment.content   = content
            comment.save()
            return JsonResponse({'MESSAGE': '댓글 수정 완료.'}, status=200) 
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'해당 게시글은 없습니다!'},status=400)
        except Comment.DoesNotExist:
            return JsonResponse({'MESSAGE':'해당 댓글은 없습니다!'},status=400)

class CommentDeleteView(View):
    @LoginConfirm
    def delete(self, request, post_id,comment_id):
        try:
            user    = request.user

            post    = Post.objects.get(id=post_id)
            comment = Comment.objects.get(id=comment_id) # 삭제하려는 댓글 조회

            if not post:
                return JsonResponse({'MESSAGE': '게시글이 존재하지 않아요.'}, status=200)

            if user.id != comment.user.id:
                return JsonResponse({'MESSAGE': '댓글 삭제 권한 없음.'}, status=403)

            comment.delete()
            return JsonResponse({'MESSAGE': f'{comment.title} 삭제 완료.'}, status=200)
        
        except Comment.DoesNotExist:
            return JsonResponse({'MESSAGE':'댓글이 없습니다.'},status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':'댓글이 없습니다.'},status=400)

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
