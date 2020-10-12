import json

from django.views import View
from django.http import JsonResponse
from posting.models import Post
from user.models import Account

class RegisterPost(View): # 게시물 등록
    def post(self, request):
        data = json.loads(request.body)

        Post.objects.create(
            account = Account(id = data['id']),
            contents = data['contents'],
            img_url = data['img_url'],
        )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status = 200)

class ViewPost(View): # 게시물 표출
    def get(self, request):
        postings = Post.objects.values()
        total_dic = {}

        account_list = Post.objects.select_related('account')
        for i in range(0, len(account_list)):
            # post_dic['id'] = account_list[i].id
            post_dic = {}
            post_dic['name'] = Account.objects.filter(id=account_list[i].account_id).get().name
            post_dic['contents'] = account_list[i].contents
            post_dic['img_url'] = account_list[i].img_url
            post_dic['create_time'] = account_list[i].create_time

            total_dic[account_list[i].id] = post_dic

        return JsonResponse({'postings':total_dic}, status = 200)
