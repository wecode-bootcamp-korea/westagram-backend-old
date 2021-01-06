import json

from datetime         import datetime
from decorator        import login_check
from django.http      import JsonResponse
from django.views     import View
from django.shortcuts import render
from user.models      import User
from .models          import Post, Image, Comment, Like, Recomment

# 게시물 등록, 전체 조회
class PostView(View):
    @login_check
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            image    = data['image']
            pub_date = datetime.now() # 2020-12-30 11:47:45.781887 -  영국시간임

            Post.objects.create(user=user, pub_date=pub_date)
            post = Post.objects.filter(user=user).last()
            Image.objects.create(post=post,image=image)

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request):
        posts  = Post.objects.all()
        images = Image.objects.all()

        posts_list  = []
        images_list = []
        for post in posts:
            posts_dict = {
                'user'     : post.user.email,
                'pub_date' : post.pub_date
            }
            posts_list.append(posts_dict)

        for image in images:
            images_dict = {
                'image'  : image.image
            }
            posts_list.append(images_dict)

        return JsonResponse({'posts':posts_list}, status=200)

# 게시물 삭제
class PostDeleteView(View):    
    @login_check
    def delete(self, request, post_id):
        try:
            data = json.loads(request.body)
            post = Post.objects.get(id=post_id)
            user = request.user

            if post.user.id == user.id:
                post.delete()
                return JsonResponse({'message':'게시물 삭제 완료'}, status=200)
            else:
                return JsonResponse({'message':'권한이 없습니다.'}, status=403)
        except Post.DoesNotExist:
            return JsonResponse({"message":'해당하는 게시물이 없습니다.'}, status=400)

# 게시물 수정
class PostUpdateView(View):
    @login_check
    def put(self, request, post_id):
        try:
            data          = json.loads(request.body)
            post_querySet = Post.objects.filter(id=post_id)
            post          = post_querySet[0]
            user          = request.user
            new_image     = data['image']
            image         = post.image_set.all()

            if post.user.id == user.id:
                post_querySet.update(pub_date = datetime.now())
                image.update(image=new_image)
                return JsonResponse({'message':'게시물 수정 완료'}, status=200)
            else:
                return JsonResponse({'message':'권한이 없습니다.'}, status=403)
                
        except Post.DoesNotExist:
            return JsonResponse({"message":'해당하는 게시물이 없습니다.'}, status=400)


# 댓글 작성, 조회
class CommentView(View):
    @login_check
    def post(self, request, post_id):
        try:
            data      = json.loads(request.body)

            Comment(
                post      = Post.objects.get(id=post_id),
                user      = request.user,
                pub_date  = datetime.now(),
                content   = data['content']
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Post.DoesNotExist :
            return JsonResponse({'message':'해당하는 게시물이 없습니다.'}, status=400)
       
    def get(self, request, post_id): # post 출력 따로 comment 출력 따로..?
        post     = Post.objects.get(id=post_id)
        user     = post.user.name
        comments = post.comment_set.all()
        pub_date = post.pub_date

        if comments.count() == 0:
            return JsonResponse({'message':'댓글이 없는 게시물입니다.'}, status=400)

        contents_list = []
        for index, comment in enumerate(comments):
            print(comment.user.id)
            contents_dict = {
                'content '+ str(index+1) : comment.content,
                'writer_id'              : comment.user.id
            }
            contents_list.append(contents_dict)

        comment_dict = {
            'post_id'  : post.id,
            'user'     : user,
            'contents' : contents_list,
            'pub_date' : pub_date 
        }

        return JsonResponse({'comment':comment_dict}, status=200)

# 댓글 삭제
class CommentDeleteView(View):
    @login_check
    def delete(self, request, post_id, comment_id):
        try:
            data    = json.loads(request.body)
            user    = request.user
            post    = Post.objects.get(id=post_id)
            comment = post.comment_set.get(id=comment_id) # post 테이블에 oneToManyField 달아줘야할까?

            if comment.user.id == user.id:
                comment.delete()
                return JsonResponse({'message':'댓글 삭제 완료'}, status=200)
            return JsonResponse({'message':'권한이 없습니다.'}, status=403)

        except Post.DoesNotExist:
            return JsonResponse({'message':'해당하는 게시물이 없습니다.'}, status=400) 
        except Comment.DoesNotExist:
            return JsonResponse({'message':'해당하는 댓글이 없습니다.'}, status=400) 

# 좋아요 하기
class LikeView(View):
    @login_check
    def post(self, request, post_id):
        try:
            data          = json.loads(request.body)
            post_querySet = Post.objects.filter(id=post_id)
            post          = post_querySet[0]
            user          = request.user

            if Like.objects.filter(post=post_id): # 좋아요 테이블에 있는 게시물일 때
                if Like.objects.filter(post=post_id, user=user.id):
                    post.likes -= 1
                    like = Like.objects.filter(post=post_id, user=user.id)
                    like.delete()
                else:
                    post.likes += 1
            else:
                Like.objects.create(post=post, user=user)
                post.likes += 1

            post_likes = Like.objects.filter(post=post_id).count()
            post_querySet.update(likes = post_likes)

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except IndexError :
            return JsonResponse({'message':'해당하는 게시물이 없습니다.'}, status=400)      

# 대댓글 달기
class RecommentView(View):
    @login_check
    def post(self, request, post_id, comment_id):
        try:
            data     = json.loads(request.body)
            comments = Comment.objects.filter(post=post_id)
            for comment in comments:
                if comment.id == comment_id:
                    Recomment(
                        post      = Post.objects.get(id=post_id),
                        user      = request.user,
                        comment   = Comment.objects.get(id=comment_id),
                        content   = data['content'],
                        pub_date  = datetime.now()
                    ).save()
                    return JsonResponse({'message':'SUCCESS'}, status=201)
    
            return JsonResponse({'message':'해당하는 댓글이 없습니다.'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except Comment.DoesNotExist :
           return JsonResponse({'message':'해당하는 게시물이 없습니다.'}, status=400)
        
