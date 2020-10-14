import json

from django.views import View
from django.http import JsonResponse

from posting.models import Post, Comment, Likes, ByComment
from user.models import Account

class RegisterPost(View): # 게시물 등록
    def post(self, request):
        data = json.loads(request.body)

        Post.objects.create(
            account  = Account(id = data['id']),
            contents = data['contents'],
            img_url  = data['img_url'],
        )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class ViewPost(View): # 게시물 표출
    def get(self, request):
        # total_dic = {}

        # account_list = Post.objects.select_related('account')
        # for i in range(0, len(account_list)):
        #     post_dic = {}
        #     post_dic['name'] = Account.objects.filter(id=account_list[i].account_id).get().name
        #     post_dic['contents'] = account_list[i].contents
        #     post_dic['img_url'] = account_list[i].img_url
        #     post_dic['create_time'] = account_list[i].create_time

        #     total_dic[account_list[i].id] = post_dic
        posting_list = Post.objects.values('account__name', 'contents', 'img_url', 'create_time')

        return JsonResponse({'postings':list(posting_list)}, status = 200)

class DeletePost(View): # 게시물 삭제
    def delete(self, request):
        data = json.loads(request.body)

        Post.objects.filter(id = data['id']).delete()

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class UpdatePost(View): # 게시물 수정
    def put(self, request):
        data = json.loads(request.body)

        post = Post.objects.filter(id = data['id']).get()
        post.contents = data['contents']
        post.save()

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class RegisterComment(View): # 댓글 등록
    def post(self, request):
        data = json.loads(request.body)

        Comment.objects.create(
            account = Account(id = data['account_id']),
            post = Post(id = data['post_id']),
            contents = data['contents'],
        )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class ViewComment(View): # 댓글 표출
    def get(self, request):
        # 1번 게시물
        comment_list = Comment.objects.filter(post=Post(id=1)).values('account__name', 'contents', 'create_time')

        return JsonResponse({'comments':list(comment_list)}, status = 200)

class DeleteComment(View): # 댓글 삭제
    def delete(self, request):
        data = json.loads(request.body)

        Comment.objects.filter(account = data['account_id'], post = data['post_id']).delete()

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class RegisterByComment(View): # 대댓글 등록
    def post(self, request):
        data = json.loads(request.body)

        ByComment.objects.create(
            comment  = Comment(id = data['comment_id']),
            account  = Account(id = data['account_id']),
            contents = data['contents'],
        )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class RegisterLikes(View): # 좋아요 등록
    def post(self, request):
        data = json.loads(request.body)

        if Likes.objects.filter(account = data['account_id'], post = data['post_id']).exists():
            like = Likes.objects.filter(account = data['account_id'], post = data['post_id'])
            like.delete()
        else:
            Likes.objects.create(
                account = Account(id = data['account_id']),
                post    = Post(id = data['post_id']),
            )
        
        count     = Likes.objects.filter(post = data['post_id']).count()
        likes_cnt = Post.objects.filter(id = data['post_id']).get()
        likes_cnt.likes_count = count
        likes_cnt.save()

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class ViewLikes(View): # 좋아요 표출
    def get(self, request):
        # 1번 게시물
        likes_count = Post.objects.filter(id=1).values('id', 'likes_count')

        return JsonResponse({'comments':list(likes_count)}, status = 200)